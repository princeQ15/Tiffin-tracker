import sqlite3
from functools import wraps
from flask import g, session, redirect, url_for, flash

# Database connection helper
def get_db():
    """Get a database connection with row factory"""
    if 'db' not in g:
        g.db = sqlite3.connect('tiffin_orders.db')
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    """Close the database connection"""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    """Execute a query and return the results"""
    db = get_db()
    cur = db.execute(query, args)
    rv = cur.fetchall()
    db.commit()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def get_user(user_id):
    """Get a user by ID"""
    return query_db('SELECT * FROM users WHERE id = ?', (user_id,), one=True)

def get_user_by_username(username):
    """Get a user by username"""
    return query_db('SELECT * FROM users WHERE username = ?', (username,), one=True)

def create_user(username, password, email, is_admin=False):
    """Create a new user"""
    from werkzeug.security import generate_password_hash
    hashed_pw = generate_password_hash(password)
    query_db(
        'INSERT INTO users (username, password, email, is_admin) VALUES (?, ?, ?, ?)',
        (username, hashed_pw, email, 1 if is_admin else 0)
    )
    return get_user_by_username(username)

def get_orders(user_id=None):
    """Get all orders or orders for a specific user"""
    if user_id:
        return query_db('SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC', (user_id,))
    return query_db('SELECT * FROM orders ORDER BY created_at DESC')

def get_order(order_id):
    """Get a specific order by ID"""
    return query_db('SELECT * FROM orders WHERE id = ?', (order_id,), one=True)

def create_order(user_id, name, phone, address, meal, quantity, delivery_time):
    """Create a new order"""
    query_db(
        '''INSERT INTO orders 
           (user_id, name, phone, address, meal, quantity, delivery_time, status, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, 'Received', datetime('now'))''',
        (user_id, name, phone, address, meal, quantity, delivery_time)
    )
    return True

def update_order_status(order_id, status):
    """Update order status"""
    query_db('UPDATE orders SET status = ? WHERE id = ?', (status, order_id))
    return True

def init_db():
    """Initialize the database with required tables"""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

# Authentication decorators
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))
        user = get_user(session['user_id'])
        if not user or not user['is_admin']:
            flash('Admin access required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

from flask import Flask, render_template, request, redirect, url_for, flash, session, g
import os
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from db_utils import get_db, close_db, query_db, get_user, get_user_by_username, create_user, get_orders, get_order, create_order, update_order_status, login_required, admin_required

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'

# Make datetime available in templates
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# Database connection management
@app.before_request
def before_request():
    g.db = get_db()

@app.teardown_appcontext
def teardown_db(exception):
    close_db(exception)

def migrate_db():
    """Update existing database schema"""
    db = get_db()
    cursor = db.cursor()
    
    # Check and update users table
    cursor.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'username' in columns and 'password' not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN password TEXT")
        cursor.execute("ALTER TABLE users ADD COLUMN email TEXT")
        cursor.execute("ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT 0")
        cursor.execute("ALTER TABLE users ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        print("Added missing columns to users table")
    
    # Check and update orders table
    cursor.execute("PRAGMA table_info(orders)")
    order_columns = [column[1] for column in cursor.fetchall()]
    
    # Add all missing columns to orders table
    required_columns = ['user_id', 'name', 'phone', 'address', 'meal', 'quantity', 'delivery_time', 'status', 'created_at']
    for column in required_columns:
        if column not in order_columns:
            if column == 'user_id':
                cursor.execute("ALTER TABLE orders ADD COLUMN user_id INTEGER")
            elif column == 'status':
                cursor.execute("ALTER TABLE orders ADD COLUMN status TEXT DEFAULT 'Received'")
            elif column == 'created_at':
                cursor.execute("ALTER TABLE orders ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
            elif column == 'quantity':
                cursor.execute("ALTER TABLE orders ADD COLUMN quantity INTEGER")
            else:
                cursor.execute(f"ALTER TABLE orders ADD COLUMN {column} TEXT")
            print(f"Added {column} column to orders table")
    
    db.commit()
    db.close()

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Create orders table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            meal TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            delivery_time TEXT NOT NULL,
            status TEXT DEFAULT 'Received',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create users table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE,
            is_admin BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form.get('email')
        
        try:
            create_user(username, password, email)
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username or email already exists.', 'danger')
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = get_user_by_username(username)
        
        if user is None or not check_password_hash(user['password'], password):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        
        session.clear()
        session['user_id'] = user['id']
        session['is_admin'] = bool(user['is_admin'])
        
        # Update last login time
        query_db('UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?', (user['id'],))
        
        flash(f'Welcome back, {username}!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    user_orders = get_orders(session['user_id'])
    return render_template('profile.html', orders=user_orders)

@app.route('/order', methods=['GET', 'POST'])
@login_required
def place_order():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        address = request.form['address']
        meal = request.form['meal']
        quantity = int(request.form['quantity'])
        delivery_time = request.form['delivery_time']
        
        create_order(session['user_id'], name, phone, address, meal, quantity, delivery_time)
        
        flash('Order placed successfully!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('order.html')

@app.route('/admin')
@admin_required
def admin():
    orders = get_orders()
    users = query_db('SELECT id, username, email, is_admin FROM users')
    return render_template('admin.html', orders=orders, users=users)

@app.route('/admin/order/<int:order_id>/update', methods=['POST'])
@admin_required
def update_order(order_id):
    status = request.form['status']
    update_order_status(order_id, status)
    flash('Order status updated!', 'success')
    return redirect(url_for('admin'))

if __name__ == '__main__':
    # Initialize database if it doesn't exist
    if not os.path.exists('tiffin_orders.db'):
        try:
            init_db()
            print("✅ Database initialized successfully")
        except Exception as e:
            print(f"❌ Error initializing database: {e}")
    
    # Always run migrations to ensure schema is up to date
    try:
        migrate_db()
        print("✅ Database migration completed")
    except Exception as e:
        print(f"⚠️ Database migration completed with warnings: {e}")
    
    # Run the app
    try:
        print("\n🚀 Starting Tiffin Tracker application...")
        print(f"🌐 Server running at: http://localhost:5000")
        print("🛑 Press Ctrl+C to stop the server\n")
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"❌ Error starting the application: {e}")

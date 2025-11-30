from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from datetime import datetime, timedelta
from functools import wraps
import os
import secrets
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask app
app = Flask(__name__)

# Security configurations
app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY') or secrets.token_hex(32),
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=30),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=False,  # Set to True in production with HTTPS
    SESSION_COOKIE_SAMESITE='Lax',
    MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB max upload size
    SQLALCHEMY_DATABASE_URI=f'sqlite:///{os.path.join(os.path.dirname(os.path.abspath(__file__)), "tiffin_orders.db")}',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

# Rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Database configuration
DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tiffin_orders.db')

# Admin credentials (in production, use a proper user database)
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD_HASH = os.environ.get('ADMIN_PASSWORD_HASH', 
    generate_password_hash('admin123', method='pbkdf2:sha256:600000'))

def get_db_connection():
    """Create and return a database connection with proper error handling."""
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        # Enable foreign key support
        conn.execute('PRAGMA foreign_keys = ON')
        return conn
    except sqlite3.Error as e:
        app.logger.error(f"Database connection error: {e}")
        raise

def init_db():
    """Initialize the database with the schema and default admin user."""
    with app.app_context():
        db = get_db_connection()
        try:
            with app.open_resource('schema.sql', mode='r') as f:
                db.cursor().executescript(f.read())
            
            # Create default admin user if not exists
            admin_hash = generate_password_hash('admin123', method='pbkdf2:sha256:600000')
            db.execute("""
                INSERT OR IGNORE INTO users (username, password_hash, is_admin)
                VALUES (?, ?, 1)
            """, ('admin', admin_hash))
            
            db.commit()
            app.logger.info("Database initialized successfully")
        except Exception as e:
            db.rollback()
            app.logger.error(f"Error initializing database: {e}")
            raise
        finally:
            db.close()

# Security middleware
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:;"
    return response

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Please log in to access this page.', 'warning')
            session['next'] = request.url
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

@app.route('/')
@login_required
def home():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get user's orders with delivery information
        cursor.execute('''
            SELECT id, meal, quantity, status, delivery_address, 
                   delivery_time, estimated_delivery, 
                   strftime('%Y-%m-%d %H:%M', date) as order_date
            FROM orders 
            WHERE user_id = ? 
            ORDER BY date DESC
        ''', (session['user_id'],))
        
        orders = [dict(row) for row in cursor.fetchall()]
        
        # Get today's date for the order form
        today = datetime.now().strftime('%Y-%m-%d')
        
        return render_template('index.html', orders=orders, today=today)
        
    except sqlite3.Error as e:
        app.logger.error(f'Database error in home route: {e}')
        flash('An error occurred while loading your orders', 'error')
        return render_template('index.html', orders=[], today=datetime.now().strftime('%Y-%m-%d'))
        
    finally:
        if 'conn' in locals():
            conn.close()

@limiter.limit('10 per minute')
@app.route('/order', methods=['POST'])
@login_required
def place_order():
    if request.method == 'POST':
        meal = request.form.get('meal')
        quantity = request.form.get('quantity')
        delivery_address = request.form.get('delivery_address')
        delivery_time = request.form.get('delivery_time')
        
        # Basic validation
        if not all([meal, quantity, delivery_address, delivery_time]):
            flash('All fields are required', 'error')
            return redirect(url_for('index'))
        
        try:
            quantity = int(quantity)
            if quantity < 1 or quantity > 10:
                raise ValueError
                
            # Calculate estimated delivery time (current time + 30-40 minutes)
            now = datetime.now()
            estimated_delivery = (now + timedelta(minutes=35)).strftime('%I:%M %p')
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Get user ID from session
            user_id = session.get('user_id')
            
            # Get user details
            cursor.execute('SELECT name, phone FROM users WHERE id = ?', (user_id,))
            user = cursor.fetchone()
            
            if not user:
                flash('User not found', 'error')
                return redirect(url_for('home'))
                
            # Insert order into database with delivery details
            cursor.execute('''
                INSERT INTO orders 
                (user_id, name, phone, meal, quantity, delivery_address, 
                 delivery_time, estimated_delivery, status, date, ip_address)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Order Placed', ?, ?)
            ''', (
                user_id,
                user['name'],
                user['phone'],
                meal,
                quantity,
                delivery_address,
                delivery_time,
                estimated_delivery,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                request.remote_addr
            ))
            
            conn.commit()
            flash('Order placed successfully!', 'success')
            return redirect(url_for('home'))
            
        except ValueError:
            flash('Invalid quantity', 'error')
            return redirect(url_for('index'))
            
        except sqlite3.Error as e:
            app.logger.error(f'Database error: {e}')
            flash('An error occurred while placing your order', 'error')
            return redirect(url_for('index'))
            
        finally:
            if 'conn' in locals():
                conn.close()

@limiter.limit('5 per minute')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Username and password are required', 'error')
            return redirect(url_for('register'))
            
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if user already exists
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        if cursor.fetchone() is not None:
            flash('Username already exists', 'error')
            return redirect(url_for('register'))
            
        # Create new user
        hashed_password = generate_password_hash(password)
        cursor.execute('INSERT INTO users (username, password_hash, is_admin) VALUES (?, ?, ?)',
                     (username, hashed_password, False))
        conn.commit()
        conn.close()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@limiter.limit('5 per minute')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = bool(user['is_admin'])
            session['logged_in'] = True
            
            if user['is_admin']:
                return redirect(url_for('admin'))
            return redirect(url_for('home'))
            next_page = session.pop('next', None) or url_for('admin')
            return redirect(next_page)
        else:
            # Simulate password verification delay to prevent timing attacks
            check_password_hash(ADMIN_PASSWORD_HASH, secrets.token_hex(16))
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    # Create a new session to prevent session fixation
    session.regenerate()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('home'))

@app.route('/admin')
@login_required
def admin():
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute("SELECT * FROM orders ORDER BY date DESC")
    orders = c.fetchall()
    conn.close()
    return render_template('admin.html', orders=orders)

def create_app():
    # Initialize database if it doesn't exist
    if not os.path.exists(DATABASE):
        init_db()
    
    # Add error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>404 - Page Not Found</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                h1 { color: #dc3545; }
                a { color: #007bff; text-decoration: none; }
            </style>
        </head>
        <body>
            <h1>404 - Page Not Found</h1>
            <p>The page you're looking for doesn't exist.</p>
            <p><a href="{{ url_for('home') }}">Go to Homepage</a></p>
        </body>
        </html>
        """, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        if 'db' in locals():
            db.rollback()
        app.logger.error(f'500 Error: {error}')
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>500 - Internal Server Error</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                h1 { color: #dc3545; }
                a { color: #007bff; text-decoration: none; }
            </style>
        </head>
        <body>
            <h1>500 - Internal Server Error</h1>
            <p>An unexpected error occurred. Please try again later.</p>
            <p><a href="{{ url_for('home') }}">Go to Homepage</a></p>
        </body>
        </html>
        """, 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    # For development
    app.run(debug=True, host='0.0.0.0', port=5000)
    
    # For production (uncomment when deploying)
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=5000)
    print("Server is running at http://127.0.0.1:5000")
    print("Admin panel: http://127.0.0.1:5000/admin")
    # serve(app, host='0.0.0.0', port=5000)

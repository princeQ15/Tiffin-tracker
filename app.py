import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import create_app, db
from config import Config
from app.models import User, Order

# Create application instance
app = create_app(Config)

# Make datetime available in templates
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

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
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('register'))
        if email and User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('register'))
        
        # Create new user
        user = User(
            username=username,
            email=email
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user is None or not user.check_password(password):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        
        session.clear()
        session['user_id'] = user.id
        session['is_admin'] = user.is_admin
        
        # Update last login time
        user.last_login = datetime.utcnow()
        db.session.commit()
        
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
    user_orders = Order.query.filter_by(user_id=session['user_id']).all()
    return render_template('profile.html', orders=user_orders)

@app.route('/order', methods=['GET', 'POST'])
@login_required
def place_order():
    if request.method == 'POST':
        order = Order(
            user_id=session['user_id'],
            name=request.form['name'],
            phone=request.form['phone'],
            address=request.form['address'],
            meal=request.form['meal'],
            quantity=int(request.form['quantity']),
            delivery_time=request.form['delivery_time'],
            status='Received'
        )
        
        db.session.add(order)
        db.session.commit()
        
        flash('Order placed successfully!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('order.html')

@app.route('/admin')
@admin_required
def admin():
    orders = Order.query.all()
    users = User.query.all()
    return render_template('admin.html', orders=orders, users=users)

@app.route('/admin/order/<int:order_id>/update', methods=['POST'])
@admin_required
def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    order.status = request.form['status']
    db.session.commit()
    
    flash('Order status updated!', 'success')
    return redirect(url_for('admin'))

# Login required decorator
def login_required(f):
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Admin required decorator
def admin_required(f):
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or not session.get('is_admin'):
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

if __name__ == '__main__':
    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()
    
    # Run the app
    try:
        print("\n🚀 Starting Tiffin Tracker application...")
        print(f"🌐 Server running at: http://localhost:5000")
        print("🛑 Press Ctrl+C to stop the server\n")
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"❌ Error starting the application: {e}")

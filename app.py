"""Main application module for the Tiffin Tracker Flask application.

This module initializes the Flask application and defines the main routes
for user authentication, order management, and admin functionality.
"""

import os
from typing import Any, Dict, Optional, Union

from flask import (
    Flask, 
    render_template, 
    request, 
    redirect, 
    url_for, 
    flash, 
    session, 
    g, 
    Response,
    abort
)
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.wrappers import Response as WsgiResponse

from app import create_app, db
from config import Config
from app.models import User, Order

# Create application instance
app = create_app(Config)

# Make datetime available in templates
@app.context_processor
def inject_now() -> Dict[str, datetime]:
    """Inject the current datetime into all templates.
    
    Returns:
        Dict[str, datetime]: A dictionary containing the current datetime 
        under the key 'now'.
    """
    return {'now': datetime.now()}

# Routes
@app.route('/')
def index() -> str:
    """Render the home page.
    
    Returns:
        str: Rendered HTML template for the home page.
    """
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register() -> Union[Response, str]:
    """Handle user registration.
    
    GET: Display the registration form.
    POST: Process the registration form and create a new user.
    
    Returns:
        Union[Response, str]: 
            - On GET: Rendered registration form template.
            - On successful POST: Redirect to login page.
            - On error: Redirect back to registration page with error message.
    """
    if request.method == 'POST':
        username: str = request.form['username']
        password: str = request.form['password']
        email: Optional[str] = request.form.get('email')
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('register'))
        if email and User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('register'))
        
        try:
            # Create new user
            user = User(username=username, email=email)
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error during registration: {str(e)}")
            flash('An error occurred during registration. Please try again.', 'danger')
            return redirect(url_for('register'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login() -> Union[Response, str]:
    """Handle user login.
    
    GET: Display the login form.
    POST: Process the login form and authenticate the user.
    
    Returns:
        Union[Response, str]: 
            - On GET: Rendered login form template.
            - On successful POST: Redirect to home page.
            - On failed authentication: Redirect back to login page with error message.
    """
    if request.method == 'POST':
        username: str = request.form['username']
        password: str = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'danger')
        flash(f'Welcome back, {username}!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('login.html')

@app.route('/logout')
def logout() -> Response:
    """Log out the current user and clear the session.
    
    Returns:
        Response: Redirect to the home page with a logout message.
    """
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile() -> str:
    """Display the user's profile page with their order history.
    
    This route is protected and requires the user to be logged in.
    
    Returns:
        str: Rendered profile template with the user's orders.
    """
    user_orders = Order.query.filter_by(user_id=session['user_id']).all()
    return render_template('profile.html', orders=user_orders)

@app.route('/order', methods=['GET', 'POST'])
@login_required
def place_order() -> Union[Response, str]:
    """Handle order placement.
    
    GET: Display the order form.
    POST: Process the order form and create a new order.
    
    Returns:
        Union[Response, str]:
            - On GET: Rendered order form template.
            - On successful POST: Redirect to profile page with success message.
    
    Note:
        This route is protected and requires the user to be logged in.
    """
    if request.method == 'POST':
        try:
            order = Order(
                user_id=session['user_id'],
                name=request.form.get('name', ''),
                phone=request.form.get('phone', ''),
                address=request.form.get('address', ''),
                meal=request.form.get('meal', ''),
                quantity=int(request.form.get('quantity', 1)),
                delivery_time=request.form.get('delivery_time', ''),
                status='Received'
            )
            
            db.session.add(order)
            db.session.commit()
            
            flash('Order placed successfully!', 'success')
            return redirect(url_for('profile'))
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error placing order: {str(e)}")
            flash('An error occurred while placing your order. Please try again.', 'danger')
    
    return render_template('order.html')

@app.route('/admin')
@admin_required
def admin() -> str:
    """Display the admin dashboard with all orders and users.
    
    This route is protected and requires admin privileges.
    
    Returns:
        str: Rendered admin template with all orders and users.
    """
    orders = Order.query.order_by(Order.created_at.desc()).all()
    users = User.query.all()
    return render_template('admin.html', orders=orders, users=users)

@app.route('/admin/order/<int:order_id>/update', methods=['POST'])
@admin_required
def update_order(order_id: int) -> Response:
    """Update the status of an order.
    
    Args:
        order_id: The ID of the order to update.
    
    Returns:
        Response: Redirect back to admin dashboard with status message.
        
    Raises:
        404: If the order with the given ID is not found.
        
    Note:
        This route is protected and requires admin privileges.
    """
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    
    if not new_status:
        flash('Status is required.', 'danger')
        return redirect(url_for('admin'))
    
    try:
        order.status = new_status
        db.session.commit()
        flash('Order status updated successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error updating order status: {str(e)}")
        flash('Failed to update order status.', 'danger')
    
    return redirect(url_for('admin'))

def login_required(f: callable) -> callable:
    """Decorator to ensure a user is logged in.
    
    Args:
        f: The view function to decorate.
        
    Returns:
        callable: The decorated function that checks for authentication.
    """
    from functools import wraps
    from flask import redirect, url_for, flash
    
    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f: callable) -> callable:
    """Decorator to ensure a user is logged in and has admin privileges.
    
    Args:
        f: The view function to decorate.
        
    Returns:
        callable: The decorated function that checks for admin status.
    """
    from functools import wraps
    from flask import redirect, url_for, flash, session
    
    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
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

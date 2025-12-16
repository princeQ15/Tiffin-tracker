from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.meal import Meal
from app.models.order import Order, OrderItem
from app import db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    meals = Meal.query.filter_by(is_available=True).all()
    return render_template('index.html', meals=meals)

@bp.route('/menu')
def menu():
    category = request.args.get('category')
    query = Meal.query.filter_by(is_available=True)
    
    if category:
        query = query.filter_by(category=category)
        
    meals = query.all()
    return render_template('menu.html', meals=meals, active_category=category)

@bp.route('/order/<int:meal_id>', methods=['GET', 'POST'])
@login_required
def order(meal_id):
    meal = Meal.query.get_or_404(meal_id)
    
    if request.method == 'POST':
        quantity = int(request.form.get('quantity', 1))
        delivery_date = request.form.get('delivery_date')
        delivery_time = request.form.get('delivery_time')
        delivery_address = request.form.get('delivery_address')
        
        if not all([delivery_date, delivery_time, delivery_address]):
            flash('Please fill in all delivery details', 'danger')
            return redirect(url_for('main.order', meal_id=meal_id))
        
        # Create new order
        order = Order(
            user_id=current_user.id,
            status='pending',
            delivery_address=delivery_address,
            delivery_date=delivery_date,
            delivery_time=delivery_time,
            total_amount=meal.price * quantity
        )
        
        # Add order item
        order_item = OrderItem(
            order=order,
            meal=meal,
            quantity=quantity
        )
        
        db.session.add(order)
        db.session.add(order_item)
        db.session.commit()
        
        flash('Order placed successfully!', 'success')
        return redirect(url_for('main.orders'))
        
    return render_template('order.html', meal=meal)

@bp.route('/orders')
@login_required
def orders():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders.html', orders=orders)

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.first_name = request.form.get('first_name', '')
        current_user.last_name = request.form.get('last_name', '')
        current_user.phone = request.form.get('phone', '')
        current_user.address = request.form.get('address', '')
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.profile'))
        
    return render_template('profile.html')

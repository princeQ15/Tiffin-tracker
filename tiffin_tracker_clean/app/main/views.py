from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from . import main
from .. import db
from ..models import Order, User
from .forms import OrderForm
from ..decorators import admin_required

@main.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    # Get today's date and calculate start and end of week
    today = datetime.utcnow().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    # Get user's orders for the current week
    orders = Order.query.filter(
        Order.user_id == current_user.id,
        Order.delivery_date.between(start_of_week, end_of_week)
    ).order_by(Order.delivery_date.asc()).all()
    
    # Group orders by day
    orders_by_day = {}
    for order in orders:
        day = order.delivery_date.strftime('%A')
        if day not in orders_by_day:
            orders_by_day[day] = []
        orders_by_day[day].append(order)
    
    return render_template('dashboard.html', 
                         orders_by_day=orders_by_day,
                         today=today)

@main.route('/order/new', methods=['GET', 'POST'])
@login_required
def new_order():
    form = OrderForm()
    if form.validate_on_submit():
        order = Order(
            user_id=current_user.id,
            name=form.name.data,
            phone=form.phone.data,
            address=form.address.data,
            meal_type=form.meal_type.data,
            quantity=form.quantity.data,
            delivery_date=form.delivery_date.data,
            delivery_time=form.delivery_time.data,
            special_instructions=form.special_instructions.data
        )
        db.session.add(order)
        db.session.commit()
        flash('Your order has been placed!', 'success')
        return redirect(url_for('main.dashboard'))
    
    # Set default values if user is logged in
    if current_user.is_authenticated:
        form.name.data = current_user.username
        # You might want to add phone and address to the User model
        # form.phone.data = current_user.phone
        # form.address.data = current_user.address
    
    return render_template('new_order.html', title='New Order', form=form)

@main.route('/order/<int:order_id>')
@login_required
def order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id and not current_user.is_admin:
        flash('You do not have permission to view this order.', 'danger')
        return redirect(url_for('main.dashboard'))
    return render_template('order.html', order=order)

@main.route('/order/<int:order_id>/cancel', methods=['POST'])
@login_required
def cancel_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id and not current_user.is_admin:
        flash('You do not have permission to cancel this order.', 'danger')
    elif order.status not in [Order.STATUS_PENDING, Order.STATUS_CONFIRMED]:
        flash('This order cannot be cancelled.', 'warning')
    else:
        order.status = Order.STATUS_CANCELLED
        db.session.commit()
        flash('Your order has been cancelled.', 'success')
    return redirect(url_for('main.dashboard'))

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    # For now, just show the profile page
    # In a real app, you'd have a form to update profile info
    return render_template('profile.html', title='My Profile')

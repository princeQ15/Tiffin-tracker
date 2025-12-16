from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app.models import User, Order, Meal, db
from functools import wraps

bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You need to be an admin to access this page.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/')
@login_required
@admin_required
def dashboard():
    total_users = User.query.count()
    total_orders = Order.query.count()
    total_meals = Meal.query.count()
    
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_orders=total_orders,
                         total_meals=total_meals,
                         recent_orders=recent_orders,
                         recent_users=recent_users)

@bp.route('/users')
@login_required
@admin_required
def users():
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('admin/users.html', users=users)

@bp.route('/orders')
@login_required
@admin_required
def orders():
    page = request.args.get('page', 1, type=int)
    orders = Order.query.order_by(Order.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('admin/orders.html', orders=orders)

@bp.route('/meals')
@login_required
@admin_required
def meals():
    meals = Meal.query.all()
    return render_template('admin/meals.html', meals=meals)

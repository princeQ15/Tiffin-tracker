from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import User, Order, Meal
from functools import wraps

bp = Blueprint('api', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/users')
@login_required
@admin_required
def get_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_admin': user.is_admin,
        'created_at': user.created_at.isoformat()
    } for user in users])

@bp.route('/orders')
@login_required
def get_orders():
    if current_user.is_admin:
        orders = Order.query.all()
    else:
        orders = Order.query.filter_by(user_id=current_user.id).all()
        
    return jsonify([{
        'id': order.id,
        'user_id': order.user_id,
        'status': order.status.value,
        'total_amount': order.total_amount,
        'created_at': order.created_at.isoformat(),
        'items': [{
            'meal_id': item.meal_id,
            'quantity': item.quantity,
            'price': item.meal.price if item.meal else 0
        } for item in order.items]
    } for order in orders])

@bp.route('/meals')
def get_meals():
    meals = Meal.query.all()
    return jsonify([{
        'id': meal.id,
        'name': meal.name,
        'description': meal.description,
        'price': meal.price,
        'image_url': meal.image_url,
        'is_available': meal.is_available
    } for meal in meals])

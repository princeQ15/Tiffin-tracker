from .user import User, Role, user_roles
from .order import Order, OrderStatus, OrderItem, Payment, PaymentStatus
from .meal import Meal, MealCategory, meal_categories

# Import all models to ensure they are registered with SQLAlchemy
__all__ = [
    'User', 'Role', 'user_roles',
    'Order', 'OrderStatus', 'OrderItem', 'Payment', 'PaymentStatus',
    'Meal', 'MealCategory', 'meal_categories'
]

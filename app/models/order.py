from datetime import datetime
from enum import Enum
from app import db


class OrderStatus(Enum):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    IN_PROGRESS = 'in_progress'
    OUT_FOR_DELIVERY = 'out_for_delivery'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'
    REFUNDED = 'refunded'


class PaymentStatus(Enum):
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'
    REFUNDED = 'refunded'
    PARTIALLY_REFUNDED = 'partially_refunded'
    CANCELLED = 'cancelled'

class Order(db.Model):
    """Order model for tiffin orders."""
    __tablename__ = 'order'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    delivery_address = db.Column(db.Text, nullable=False)
    delivery_date = db.Column(db.Date, nullable=False)
    delivery_time = db.Column(db.String(50), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Order {self.id}>'
    
    def calculate_total(self):
        """Calculate the total amount for the order."""
        self.total_amount = sum(item.quantity * item.meal.price for item in self.items)
        return self.total_amount
    
    def to_dict(self):
        """Convert order to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'status': self.status.value if self.status else None,
            'delivery_address': self.delivery_address,
            'delivery_date': self.delivery_date.isoformat() if self.delivery_date else None,
            'delivery_time': self.delivery_time,
            'total_amount': self.total_amount,
            'created_at': self.created_at.isoformat(),
            'items': [item.to_dict() for item in self.items]
        }


class OrderItem(db.Model):
    """Order items model for individual items in an order."""
    __tablename__ = 'order_item'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)


class Payment(db.Model):
    """Payment model for order payments."""
    __tablename__ = 'payment'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.Enum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)
    transaction_id = db.Column(db.String(100), unique=True, nullable=True)
    payment_method = db.Column(db.String(50), nullable=False)  # credit_card, debit_card, upi, net_banking, etc.
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    order = db.relationship('Order', backref=db.backref('payments', lazy=True))
    
    def __repr__(self):
        return f'<Payment {self.id} - {self.status} - {self.amount}>'
    
    def to_dict(self):
        """Convert payment to dictionary."""
        return {
            'id': self.id,
            'order_id': self.order_id,
            'amount': self.amount,
            'status': self.status.value if self.status else None,
            'transaction_id': self.transaction_id,
            'payment_method': self.payment_method,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None
        }
    
    # Relationships
    meal = db.relationship('Meal')
    
    def __repr__(self):
        return f'<OrderItem {self.id}>'
    
    def to_dict(self):
        """Convert order item to dictionary."""
        return {
            'id': self.id,
            'meal_id': self.meal_id,
            'meal_name': self.meal.name if self.meal else None,
            'quantity': self.quantity,
            'unit_price': self.meal.price if self.meal else 0,
            'total_price': self.meal.price * self.quantity if self.meal else 0
        }

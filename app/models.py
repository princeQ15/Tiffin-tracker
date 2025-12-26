"""Database models for the Tiffin Tracker application.

This module defines the SQLAlchemy models for the application, including
User and Order models with their respective relationships and helper methods.
"""

from datetime import datetime
from typing import Dict, Any, Optional

from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

from . import db

class User(db.Model):
    """User model representing a registered user in the system.
    
    Attributes:
        id (int): Primary key.
        username (str): Unique username for the user.
        email (Optional[str]): User's email address (optional).
        password_hash (str): Hashed password for security.
        is_admin (bool): Whether the user has admin privileges.
        created_at (datetime): Timestamp when the user was created.
        last_login (Optional[datetime]): Timestamp of the user's last login.
        orders (List[Order]): List of orders placed by the user.
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    orders = db.relationship('Order', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password: str) -> None:
        """Set the user's password.
        
        Args:
            password (str): The plain text password to hash and store.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Check if the provided password matches the stored hash.
        
        Args:
            password (str): The plain text password to verify.
            
        Returns:
            bool: True if the password is correct, False otherwise.
        """
        return check_password_hash(self.password_hash, password)
        
    def __repr__(self) -> str:
        """Return a string representation of the User instance.
        
        Returns:
            str: A string in the format '<User username>'
        """
        return f'<User {self.username}>'

class Order(db.Model):
    """Order model representing a food delivery order in the system.
    
    Attributes:
        id (int): Primary key.
        user_id (int): Foreign key referencing the user who placed the order.
        name (str): Name of the person placing the order.
        phone (str): Contact phone number for the order.
        address (str): Delivery address for the order.
        meal (str): Type of meal being ordered.
        quantity (int): Number of meals ordered.
        delivery_time (str): Requested delivery time.
        status (str): Current status of the order (e.g., 'Received', 'Preparing', 'On the way', 'Delivered', 'Cancelled').
        created_at (datetime): Timestamp when the order was created.
    """
    __tablename__ = 'orders'
    
    # Status constants
    STATUS_RECEIVED = 'Received'
    STATUS_PREPARING = 'Preparing'
    STATUS_ON_THE_WAY = 'On the way'
    STATUS_DELIVERED = 'Delivered'
    STATUS_CANCELLED = 'Cancelled'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    meal = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    delivery_time = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default=STATUS_RECEIVED)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the order object to a dictionary.
        
        Returns:
            Dict[str, Any]: A dictionary representation of the order.
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'phone': self.phone,
            'address': self.address,
            'meal': self.meal,
            'quantity': self.quantity,
            'delivery_time': self.delivery_time,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
    def __repr__(self) -> str:
        """Return a string representation of the Order instance.
        
        Returns:
            str: A string in the format '<Order id by user_id>'
        """
        return f'<Order {self.id} by {self.user_id}>'

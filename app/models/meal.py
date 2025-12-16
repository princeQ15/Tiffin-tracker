from datetime import datetime
from enum import Enum
from decimal import Decimal
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Text, Boolean, DateTime, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.hybrid import hybrid_property
from app import db

# Association table for many-to-many relationship between meals and categories
meal_categories = db.Table(
    'meal_categories',
    db.Column('meal_id', db.Integer, db.ForeignKey('meal.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('meal_category.id'), primary_key=True)
)

class MealCategory(db.Model):
    """Meal category model (e.g., Vegetarian, Non-Vegetarian, Vegan, etc.)."""
    __tablename__ = 'meal_category'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    display_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    meals = db.relationship('Meal', secondary=meal_categories, back_populates='categories')
    
    def __repr__(self):
        return f'<MealCategory {self.name}>'
    
    @classmethod
    def get_active_categories(cls):
        """Get all active categories ordered by display_order."""
        return cls.query.filter_by(is_active=True).order_by(cls.display_order).all()


class Meal(db.Model):
    """Meal model for tiffin menu items."""
    __tablename__ = 'meal'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    is_vegetarian = db.Column(db.Boolean, default=False)
    is_available = db.Column(db.Boolean, default=True)
    image_url = db.Column(db.String(255))
    category = db.Column(db.String(50))  # veg, non-veg, vegan, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    order_items = db.relationship('OrderItem', backref='meal', lazy=True)
    
    def __repr__(self):
        return f'<Meal {self.name}>'
    
    def to_dict(self):
        """Convert meal to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'is_vegetarian': self.is_vegetarian,
            'is_available': self.is_available,
            'image_url': self.image_url,
            'category': self.category
        }


class MealReview(db.Model):
    """Customer reviews for meals."""
    __tablename__ = 'meal_review'
    
    id = db.Column(db.Integer, primary_key=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text)
    is_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    meal = db.relationship('Meal', backref=db.backref('reviews', lazy=True))
    user = db.relationship('User')
    
    def __repr__(self):
        return f'<MealReview {self.rating} stars for {self.meal.name}>'

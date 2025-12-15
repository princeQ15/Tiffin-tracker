from datetime import datetime, timedelta
import jwt
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager, bcrypt

# Association table for many-to-many relationship between users and roles
user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)
)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(255))
    users = db.relationship('User', secondary=user_roles, back_populates='roles')
    
    def __repr__(self):
        return f'<Role {self.name}>'

class User(UserMixin, db.Model):
    """User account model."""
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    phone = db.Column(db.String(20))
    address = db.Text()
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    orders = db.relationship('Order', backref='customer', lazy=True)
    roles = db.relationship('Role', secondary=user_roles, back_populates='users')
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        """Create hashed password."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """Check hashed password."""
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def get_reset_token(self, expires_sec=1800):
        """Generate a password reset token."""
        reset_token = jwt.encode(
            {
                'user_id': self.id,
                'exp': datetime.utcnow() + timedelta(seconds=expires_sec)
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        return reset_token

    @staticmethod
    def verify_reset_token(token):
        """Verify the password reset token."""
        try:
            user_id = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    def get_full_name(self):
        """Return the full name of the user."""
        return f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else self.username
    
    @classmethod
    def get_by_email(cls, email):
        """Get user by email."""
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def get_by_username(cls, username):
        """Get user by username."""
        return cls.query.filter_by(username=username).first()


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login."""
    return User.query.get(int(user_id))

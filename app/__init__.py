import os
from flask import Flask, current_app, request, session, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from flask_seasurf import SeaSurf
from flask_session import Session
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from config import Config

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
login_manager.session_protection = 'strong'

# Email configuration
mail = Mail()

# CSRF Protection
csrf = CSRFProtect()

# Rate limiting
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Security headers
talisman = Talisman()

# Session configuration
session = Session()

# Content Security Policy
csp = {
    'default-src': [
        '\'self\'',
        'cdn.jsdelivr.net',
        'cdnjs.cloudflare.com',
        'fonts.googleapis.com',
        'fonts.gstatic.com',
        'data:',
        '\'unsafe-inline\''  # Required for some inline styles/scripts
    ],
    'img-src': [
        '\'self\'',
        'data:',
        'blob:'
    ],
    'script-src': [
        '\'self\'',
        'cdn.jsdelivr.net',
        'cdnjs.cloudflare.com',
        '\'unsafe-inline\'',
        '\'unsafe-eval\''
    ],
    'style-src': [
        '\'self\'',
        'cdn.jsdelivr.net',
        'fonts.googleapis.com',
        '\'unsafe-inline\''
    ],
    'font-src': [
        '\'self\'',
        'fonts.gstatic.com',
        'cdn.jsdelivr.net',
        'data:'
    ]
}

def create_app(config_class=Config):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    
    # Initialize Flask-Migrate
    migrate = Migrate(app, db)
    
    # Initialize rate limiting
    limiter.init_app(app)
    
    # Initialize security headers with CSP
    talisman.init_app(
        app,
        force_https=app.config.get('ENV') == 'production',
        strict_transport_security=True,
        session_cookie_secure=True,
        content_security_policy=csp,
        content_security_policy_nonce_in=['script-src']
    )
    
    # Initialize session
    session.init_app(app)
    
    # Register blueprints
    from app.routes import main, auth, admin, api
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp, url_prefix='/auth')
    app.register_blueprint(admin.bp, url_prefix='/admin')
    app.register_blueprint(api.bp, url_prefix='/api/v1')
    
    # Error handlers
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    
    # Shell context
    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': models.User,
            'Order': models.Order,
            'Meal': models.Meal
        }
    
    # Request hooks
    @app.before_request
    def before_request():
        # Set session timeout to 30 minutes
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=30)
        
        # Track user activity
        if current_user.is_authenticated:
            current_user.last_seen = datetime.utcnow()
            db.session.commit()
    
    return app

# Import models at the bottom to avoid circular imports
from app import models

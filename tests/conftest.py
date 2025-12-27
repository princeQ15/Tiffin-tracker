"""Pytest configuration and fixtures for testing the Tiffin Tracker application.

This module provides test fixtures and configuration for the test suite.
It sets up a test database, provides test clients, and handles test isolation.
"""

import os
import sys
from typing import Generator, Dict, Any

import pytest
from flask import Flask, Response
from flask.testing import FlaskClient, FlaskCliRunner
from flask_login import LoginManager, login_user

# Add the project root to the Python path to enable absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the db instance from the app
from app import db

# Initialize login manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

# Import models after db is defined to avoid circular imports
from app.models import User, Order


def create_test_app(config: Dict[str, Any] = None) -> Flask:
    """Create and configure a Flask application for testing.
    
    Args:
        config: Optional configuration overrides for the test app.
        
    Returns:
        Flask: A configured Flask application instance for testing.
    """
    app = Flask(__name__)
    
    # Default configuration
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        WTF_CSRF_ENABLED=False,
        SECRET_KEY='test-secret-key',
        LOGIN_DISABLED=False
    )
    
    # Apply any custom config overrides
    if config:
        app.config.update(config)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Register blueprints (if any)
    from app.routes.auth import bp as auth_bp
    from app.routes.main import bp as main_bp
    from app.routes.admin import bp as admin_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    
    return app

@pytest.fixture(scope='module')
def app() -> Generator[Flask, None, None]:
    """Create and configure a new app instance for testing.
    
    This fixture creates a fresh Flask application with a clean database for each test module.
    It handles setup and teardown of the application context and database.
    
    Yields:
        Flask: The test application instance.
    """
    # Create the test app
    app = create_test_app()
    
    # Create an application context
    with app.app_context():
        # Create all database tables
        db.create_all()
        
        # Add test users
        test_user = User(
            username='testuser',
            email='test@example.com',
            is_admin=False
        )
        test_user.set_password('testpass123')
        
        # Add admin user
        admin_user = User(
            username='admin',
            email='admin@example.com',
            is_admin=True
        )
        admin_user.set_password('adminpass123')
        
        # Add test orders
        order1 = Order(
            user_id=1,  # testuser
            name='Test User',
            phone='1234567890',
            address='123 Test St',
            meal='Test Meal',
            quantity=2,
            delivery_time='12:00 PM',
            status='Received'
        )
        
        # Add all to session and commit
        db.session.add_all([test_user, admin_user, order1])
        db.session.commit()
        
        yield app
        
        # Clean up
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """Create a test client for the app.
    
    Args:
        app: The test Flask application.
        
    Returns:
        FlaskClient: A test client for making requests to the app.
    """
    return app.test_client()


@pytest.fixture
def runner(app: Flask) -> FlaskCliRunner:
    """Create a CLI runner for testing Click commands.
    
    Args:
        app: The test Flask application.
        
    Returns:
        FlaskCliRunner: A test runner for CLI commands.
    """
    return app.test_cli_runner()


@pytest.fixture
def auth_client(client: FlaskClient, app: Flask) -> FlaskClient:
    """Create an authenticated test client.
    
    Args:
        client: The test client fixture.
        app: The test Flask application.
        
    Returns:
        FlaskClient: An authenticated test client.
    """
    with client:
        # Login the test user
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'testpass123'
        }, follow_redirects=True)
        
        # Verify login was successful
        assert response.status_code == 200
        assert b'Logged in successfully' in response.data
        
        yield client
        
        # Logout after the test
        client.get('/logout')


@pytest.fixture
def admin_client(client: FlaskClient, app: Flask) -> FlaskClient:
    """Create an authenticated test client with admin privileges.
    
    Args:
        client: The test client fixture.
        app: The test Flask application.
        
    Returns:
        FlaskClient: An authenticated admin test client.
    """
    with client:
        # Login the admin user
        response = client.post('/login', data={
            'username': 'admin',
            'password': 'adminpass123'
        }, follow_redirects=True)
        
        # Verify admin login was successful
        assert response.status_code == 200
        assert b'Logged in successfully' in response.data
        
        yield client
        
        # Logout after the test
        client.get('/logout')


@pytest.fixture
def test_user(app: Flask) -> User:
    """Get the test user from the database.
    
    Args:
        app: The test Flask application.
        
    Returns:
        User: The test user instance.
    """
    with app.app_context():
        return User.query.filter_by(username='testuser').first()


@pytest.fixture
def test_admin(app: Flask) -> User:
    """Get the test admin user from the database.
    
    Args:
        app: The test Flask application.
        
    Returns:
        User: The test admin user instance.
    """
    with app.app_context():
        return User.query.filter_by(username='admin').first()


@pytest.fixture
def test_order(app: Flask) -> Order:
    """Get a test order from the database.
    
    Args:
        app: The test Flask application.
        
    Returns:
        Order: A test order instance.
    """
    with app.app_context():
        return Order.query.first()

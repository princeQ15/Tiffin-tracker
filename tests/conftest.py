import os
import sys
import tempfile
import pytest

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import after adding to path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

# Import models after db is defined
from app.models.user import User

def create_test_app():
    """Create a Flask application for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SECRET_KEY'] = 'test-secret-key'
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Register blueprints and routes would go here
    
    return app

@pytest.fixture(scope='module')
def app():
    """Create and configure a new app instance for testing."""
    app = create_test_app()
    
    # Create test client and context
    ctx = app.app_context()
    ctx.push()
    
    # Create tables and add test data
    db.create_all()
    user = User(username='testuser', email='test@example.com')
    user.set_password('testpass123')
    db.session.add(user)
    db.session.commit()

    yield app
    
    # Clean up
    db.session.remove()
    db.drop_all()
    ctx.pop()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

@pytest.fixture
def auth_client(client):
    """A test client with an authenticated user."""
    client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass123'
    }, follow_redirects=True)
    return client

import os
import pytest
from app import create_app, db
from app.models.user import User

@pytest.fixture
def app():
    """Create and configure a new app instance for testing."""
    # Use a separate test configuration
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret-key'
    })

    # Create the database and load test data
    with app.app_context():
        db.create_all()
        # Create a test user
        user = User(username='testuser', email='test@example.com')
        user.set_password('testpass123')
        db.session.add(user)
        db.session.commit()

    yield app

    # Clean up after the test
    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

class TestBasicFunctionality:
    """Test basic application functionality."""

    def test_app_exists(self, app):
        """Test that the app is created."""
        assert app is not None

    def test_home_page(self, client):
        """Test that the home page loads."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Tiffin Tracker' in response.data

    def test_login_page(self, client):
        """Test that the login page loads."""
        response = client.get('/login')
        assert response.status_code == 200
        assert b'Login' in response.data

    def test_valid_login(self, client):
        """Test that a user can log in with valid credentials."""
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'testpass123'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'Logout' in response.data  # Check for logout button

    def test_invalid_login(self, client):
        """Test that invalid login fails."""
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        assert b'Invalid username or password' in response.data

    def test_protected_route_unauthorized(self, client):
        """Test that protected routes redirect to login when not authenticated."""
        response = client.get('/profile', follow_redirects=True)
        assert b'Please log in to access this page' in response.data

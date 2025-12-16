"""Test authentication routes and functionality."""
import pytest
from flask import url_for
from app.models.user import User

def test_user_registration(client, db):
    """Test user registration."""
    response = client.post('/register', data={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'testpass123',
        'confirm_password': 'testpass123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Account created' in response.data
    
    # Verify user was created in the database
    user = User.query.filter_by(email='newuser@example.com').first()
    assert user is not None
    assert user.username == 'newuser'

def test_user_login(client, db):
    """Test user login."""
    # First register a user
    client.post('/register', data={
        'username': 'testlogin',
        'email': 'testlogin@example.com',
        'password': 'testpass123',
        'confirm_password': 'testpass123'
    })
    
    # Now try to login
    response = client.post('/login', data={
        'email': 'testlogin@example.com',
        'password': 'testpass123',
        'remember': False
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Welcome back' in response.data

def test_register(client, app):
    """Test that a user can register successfully."""
    # Test registration with valid data
    response = client.post('/register', data={
        'username': 'testuser',
        'password': 'testpass',
        'confirm_password': 'testpass',
        'email': 'test@example.com',
        'full_name': 'Test User'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Registration successful' in response.data
    
    # Verify user was added to the database
    with app.app_context():
        user = get_db().execute(
            'SELECT * FROM user WHERE username = ?', ('testuser',)
        ).fetchone()
        assert user is not None
        assert user['username'] == 'testuser'

def test_register_duplicate_username(client):
    """Test that duplicate usernames are not allowed."""
    # First registration should succeed
    client.post('/register', data={
        'username': 'duplicate',
        'password': 'testpass',
        'confirm_password': 'testpass',
        'email': 'test@example.com',
        'full_name': 'Test User'
    })
    
    # Second registration with same username should fail
    response = client.post('/register', data={
        'username': 'duplicate',
        'password': 'testpass',
        'confirm_password': 'testpass',
        'email': 'test2@example.com',
        'full_name': 'Test User 2'
    })
    
    assert b'Username already exists' in response.data

def test_login_logout(client, auth):
    """Test that a user can log in and log out."""
    # Register a test user
    auth.register('testuser', 'testpass')
    
    # Test login with valid credentials
    response = auth.login('testuser', 'testpass')
    assert response.status_code == 302  # Redirect after login
    
    # Test that the user is logged in
    response = client.get('/profile')
    assert b'Profile' in response.data
    
    # Test logout
    response = auth.logout()
    assert response.status_code == 302  # Redirect after logout
    
    # Test that the user is logged out
    response = client.get('/profile')
    assert response.status_code == 302  # Should redirect to login
    assert '/login' in response.location

def test_login_invalid_credentials(auth):
    """Test that login fails with invalid credentials."""
    # Test with non-existent user
    response = auth.login('nonexistent', 'password')
    assert b'Invalid username or password' in response.data
    
    # Test with wrong password
    auth.register('testuser', 'testpass')
    response = auth.login('testuser', 'wrongpass')
    assert b'Invalid username or password' in response.data

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required'),
    ('a', '', b'Password is required'),
    ('test', 'test', b'Passwords must match'),
))
def test_register_validate_input(auth, username, password, message):
    """Test registration input validation."""
    response = auth.register(
        username, 
        password, 
        confirm_password=password,
        email='test@example.com',
        full_name='Test User'
    )
    assert message in response.data

@pytest.mark.parametrize(('username', 'email', 'password', 'message'), (
    ('', '', '', b'This field is required'),
    ('test', 'invalid-email', 'test', b'Invalid email address'),
    ('test', 'test@example.com', 'short', b'Field must be at least 8 characters'),
    ('test', 'test@example.com', 'testpass123', b'Email already registered'),
))
def test_register_validate_input(client, username, email, password, message):
    """Test registration form validation."""
    # First create a user with test@example.com
    client.post('/register', data={
        'username': 'existing',
        'email': 'test@example.com',
        'password': 'testpass123',
        'confirm_password': 'testpass123'
    })
    
    # Test validation
    response = client.post('/register', data={
        'username': username,
        'email': email,
        'password': password,
        'confirm_password': password
    }, follow_redirects=True)
    
    assert message in response.data

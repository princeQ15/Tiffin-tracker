"""Test cases for the Tiffin Tracker application.

This module contains tests for the main application functionality including:
- Application configuration and setup
- Public routes (home, about, contact)
- Authentication flows
- Protected routes
- Error handling
- Static file serving
"""
from typing import Dict, Any, Optional

import pytest
from flask import Flask, Response
from flask.testing import FlaskClient

from app.models import User, Order
from app import db


def test_app_creation(app: Flask) -> None:
    """Test that the app is created with the correct configuration.
    
    Verifies that the application is properly configured for testing
    with all required configuration values set.
    """
    # Assert app exists and has required config
    assert app is not None, "App instance should be created"
    
    # Test configuration
    assert app.config['TESTING'] is True, "App should be in testing mode"
    assert app.config['WTF_CSRF_ENABLED'] is False, "CSRF should be disabled in testing"
    assert 'SECRET_KEY' in app.config, "Secret key should be configured"
    assert 'SQLALCHEMY_DATABASE_URI' in app.config, "Database URI should be configured"
    
    # Verify extensions are initialized
    assert hasattr(app, 'extensions'), "App should have extensions"
    assert 'sqlalchemy' in app.extensions, "SQLAlchemy should be initialized"
    assert 'login_manager' in app.extensions, "LoginManager should be initialized"

@pytest.mark.parametrize('route,expected_elements', [
    # Home page
    ('/', [b'Tiffin Tracker', b'Welcome', b'Login', b'Register']),
    # About page
    ('/about', [b'About Us', b'Our Mission']),
    # Contact page
    ('/contact', [b'Contact Us', b'Get in Touch']),
])
def test_public_pages(client: FlaskClient, route: str, expected_elements: list[bytes]) -> None:
    """Test that public pages load successfully with expected content.
    
    Verifies that all public routes return a 200 status code and contain
    the expected elements in their response.
    """
    # Act
    response = client.get(route)
    
    # Assert
    assert response.status_code == 200, f"{route} should return 200 OK"
    for element in expected_elements:
        assert element in response.data, f"{element!r} should be in {route} response"

@pytest.mark.parametrize('route,expected_status,expected_content', [
    # Non-existent route
    ('/non-existent-route', 404, b'Page Not Found'),
    # Invalid order ID
    ('/order/999999', 404, b'Order not found'),
    # Invalid user profile
    ('/user/nonexistent', 404, b'User not found'),
])
def test_error_pages(
    client: FlaskClient, 
    route: str, 
    expected_status: int, 
    expected_content: bytes
) -> None:
    """Test error pages and error handling.
    
    Verifies that the application properly handles and displays errors
    for various error conditions.
    """
    # Act
    response = client.get(route, follow_redirects=True)
    
    # Assert
    assert response.status_code == expected_status, \
        f"Expected status {expected_status} for {route}"
    assert expected_content in response.data, \
        f"Expected content {expected_content!r} not found in response"

@pytest.mark.parametrize('path,content_type', [
    # CSS files
    ('/static/css/style.css', 'text/css; charset=utf-8'),
    # JavaScript files
    ('/static/js/main.js', 'application/javascript'),
    # Images
    ('/static/images/logo.png', 'image/png'),
    # Favicon
    ('/favicon.ico', 'image/x-icon'),
])
def test_static_files(client: FlaskClient, path: str, content_type: str) -> None:
    """Test that static files are served correctly.
    
    Verifies that all required static assets are properly served
    with the correct content types.
    """
    # Act
    response = client.get(path)
    
    # Assert
    assert response.status_code == 200, f"{path} should be accessible"
    assert response.content_type == content_type, \
        f"{path} should have content type {content_type}"

def test_login_page(client: FlaskClient) -> None:
    """Test that the login page loads with all required elements.
    
    Verifies that the login page contains all necessary form fields
    and interactive elements.
    """
    # Act
    response = client.get('/auth/login')
    
    # Assert
    assert response.status_code == 200, "Login page should load successfully"
    
    # Check for required elements
    required_elements = [
        b'Login',
        b'name="username"',
        b'name="password"',
        b'type="submit"',
        b'Remember me',
        b'Forgot Password',
        b'Register'
    ]
    
    for element in required_elements:
        assert element in response.data, f"Element {element!r} not found in login page"

def test_valid_login_redirects_to_dashboard(client: FlaskClient, test_user: User) -> None:
    """Test that successful login redirects to the dashboard.
    
    Verifies that after a successful login, the user is redirected
    to their dashboard and the session is properly set.
    """
    # Act
    response = client.post(
        '/auth/login',
        data={
            'username': 'testuser',
            'password': 'testpass123',
            'remember': False
        },
        follow_redirects=True
    )
    
    # Assert
    assert response.status_code == 200, "Should redirect to dashboard after login"
    assert b'Dashboard' in response.data, "Dashboard should be displayed"
    
    # Verify session is set
    with client.session_transaction() as session:
        assert 'user_id' in session, "User ID should be in session"
        assert session['_fresh'] is True, "Session should be fresh"

@pytest.mark.parametrize('username,password,expected_error', [
    # Wrong password
    ('testuser', 'wrongpass', b'Invalid username or password'),
    # Non-existent user
    ('nonexistent', 'password', b'Invalid username or password'),
    # Empty fields
    ('', 'password', b'This field is required'),
    ('testuser', '', b'This field is required'),
])
def test_invalid_login_attempts(
    client: FlaskClient, 
    test_user: User,
    username: str, 
    password: str, 
    expected_error: bytes
) -> None:
    """Test various invalid login scenarios.
    
    Verifies that the application properly handles and displays
    appropriate error messages for invalid login attempts.
    """
    # Act
    response = client.post(
        '/auth/login',
        data={'username': username, 'password': password},
        follow_redirects=True
    )
    
    # Assert
    assert response.status_code == 200, "Should stay on login page"
    assert expected_error in response.data, "Expected error message not found"
    
    # Verify session is not set
    with client.session_transaction() as session:
        assert 'user_id' not in session, "User should not be logged in"

@pytest.mark.parametrize('route,expected_redirect', [
    # User profile
    ('/profile', '/auth/login?next=%2Fprofile'),
    # Order history
    ('/orders', '/auth/login?next=%2Forders'),
    # Settings
    ('/settings', '/auth/login?next=%2Fsettings'),
])
def test_protected_routes_require_authentication(
    client: FlaskClient, 
    route: str, 
    expected_redirect: str
) -> None:
    """Test that protected routes redirect to login when not authenticated.
    
    Verifies that unauthenticated users are redirected to the login page
    with a proper 'next' parameter for redirecting back after login.
    """
    # Act
    response = client.get(route, follow_redirects=False)
    
    # Assert
    assert response.status_code == 302, "Should redirect to login"
    assert expected_redirect in response.location, "Should redirect to login with next parameter"


def test_authenticated_user_redirected_from_login(auth_client: FlaskClient) -> None:
    """Test that authenticated users are redirected from login/register pages."""
    # Act - Try to access login page when already logged in
    response = auth_client.get('/auth/login', follow_redirects=True)
    
    # Assert - Should be redirected to dashboard
    assert response.status_code == 200
    assert b'Dashboard' in response.data
    assert b'You are already logged in' in response.data


def test_admin_routes_require_admin_role(admin_client: FlaskClient, client: FlaskClient) -> None:
    """Test that admin-only routes are protected."""
    # Test admin route with regular user (should be forbidden)
    response = client.get('/admin/dashboard', follow_redirects=True)
    assert response.status_code == 403, "Regular users should not access admin area"
    
    # Test admin route with admin user (should succeed)
    response = admin_client.get('/admin/dashboard', follow_redirects=True)
    assert response.status_code == 200
    assert b'Admin Dashboard' in response.data


def test_session_security(client: FlaskClient, test_user: User) -> None:
    """Test session security features."""
    # First log in to get a session
    client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'testpass123'
    }, follow_redirects=True)
    
    # Get session cookie
    session_cookie = client.cookie_jar._cookies['localhost.local']['/'].get('session')
    assert session_cookie is not None, "Session cookie should be set"
    
    # Change password (should invalidate other sessions)
    new_password = 'NewSecurePass123!'
    client.post('/settings/change-password', data={
        'current_password': 'testpass123',
        'new_password': new_password,
        'confirm_password': new_password
    }, follow_redirects=True)
    
    # Try to access protected route with old session (should fail)
    response = client.get('/profile', follow_redirects=True)
    assert b'Please log in to access this page' in response.data, "Old session should be invalidated"


def test_rate_limiting(client: FlaskClient) -> None:
    """Test that rate limiting is working for authentication endpoints."""
    # Try multiple login attempts with wrong credentials
    for _ in range(10):
        client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'wrongpassword'
        })
    
    # Next attempt should be rate limited
    response = client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'testpass123'
    })
    
    assert response.status_code == 429, "Should be rate limited after too many attempts"
    assert b'Too many login attempts' in response.data

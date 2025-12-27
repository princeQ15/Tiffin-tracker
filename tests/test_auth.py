"""Test authentication routes and functionality for the Tiffin Tracker application.

This module contains tests for user registration, login, logout, and related
authentication functionality. It includes tests for both successful operations
and various error cases.
"""
from typing import Dict, Any, Optional

import pytest
from flask import Flask, Response
from flask.testing import FlaskClient
from werkzeug.datastructures import ImmutableMultiDict

from app.models import User
from app import db


def test_user_registration_success(client: FlaskClient) -> None:
    """Test successful user registration.
    
    Verifies that a new user can register with valid credentials and that the
    user is properly created in the database.
    """
    # Arrange
    user_data = {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'TestPass123!',
        'confirm_password': 'TestPass123!',
        'full_name': 'New User',
        'phone': '+1234567890'
    }
    
    # Act
    response = client.post(
        '/auth/register',
        data=user_data,
        follow_redirects=True
    )
    
    # Assert
    assert response.status_code == 200, "Registration should complete successfully"
    assert b'Registration successful' in response.data, \
        "Success message should be displayed"
    
    # Verify user was created in the database
    user = User.query.filter_by(email='newuser@example.com').first()
    assert user is not None, "User should exist in the database"
    assert user.username == 'newuser', "Username should match"
    assert user.check_password('TestPass123!'), "Password should be hashed and verified"
    assert user.full_name == 'New User', "Full name should be saved"
    assert not user.is_admin, "New users should not be admins by default"

def test_user_login_success(client: FlaskClient, test_user: User) -> None:
    """Test successful user login with valid credentials.
    
    Verifies that an existing user can log in with correct credentials
    and is redirected to the appropriate page.
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
    assert response.status_code == 200, "Login should be successful"
    assert b'Logged in successfully' in response.data, \
        "Success message should be displayed"
    assert b'Welcome, testuser' in response.data, \
        "User should be greeted by username"


def test_login_with_remember_me(client: FlaskClient, test_user: User) -> None:
    """Test login with 'Remember Me' option enabled."""
    # Act
    response = client.post(
        '/auth/login',
        data={
            'username': 'testuser',
            'password': 'testpass123',
            'remember': True
        },
        follow_redirects=True
    )
    
    # Assert
    assert response.status_code == 200
    assert 'remember_token' in client.cookie_jar._cookies['localhost.local']['/'].keys(), \
        "Remember token cookie should be set"

@pytest.mark.parametrize('user_data,expected_message', [
    # Missing required fields
    (
        {
            'username': '',
            'password': 'TestPass123!',
            'confirm_password': 'TestPass123!',
            'email': 'test@example.com',
            'full_name': 'Test User'
        },
        b'This field is required.'
    ),
    # Invalid email format
    (
        {
            'username': 'testuser',
            'password': 'TestPass123!',
            'confirm_password': 'TestPass123!',
            'email': 'invalid-email',
            'full_name': 'Test User'
        },
        b'Invalid email address.'
    ),
    # Password too short
    (
        {
            'username': 'testuser',
            'password': 'short',
            'confirm_password': 'short',
            'email': 'test@example.com',
            'full_name': 'Test User'
        },
        b'Field must be at least 8 characters long.'
    ),
    # Passwords don't match
    (
        {
            'username': 'testuser',
            'password': 'TestPass123!',
            'confirm_password': 'DifferentPass123!',
            'email': 'test@example.com',
            'full_name': 'Test User'
        },
        b'Passwords must match.'
    ),
    # Weak password (no special char)
    (
        {
            'username': 'testuser',
            'password': 'WeakPassword1',
            'confirm_password': 'WeakPassword1',
            'email': 'test@example.com',
            'full_name': 'Test User'
        },
        b'Password must contain at least one special character.'
    )
])
def test_register_validation_errors(
    client: FlaskClient, 
    user_data: Dict[str, str], 
    expected_message: bytes
) -> None:
    """Test registration form validation with various invalid inputs."""
    # Act
    response = client.post(
        '/auth/register',
        data=user_data,
        follow_redirects=True
    )
    
    # Assert
    assert response.status_code == 200, "Form should be re-rendered with errors"
    assert expected_message in response.data, "Expected error message not found"

@pytest.mark.parametrize('field,value,error_message', [
    ('username', 'testuser', b'Username is already taken'),
    ('email', 'test@example.com', b'Email is already registered')
])
def test_register_duplicate_fields(
    client: FlaskClient, 
    test_user: User,
    field: str, 
    value: str, 
    error_message: bytes
) -> None:
    """Test that duplicate usernames and emails are not allowed during registration."""
    # Arrange - test_user fixture already created with username 'testuser' and email 'test@example.com'
    user_data = {
        'username': 'unique_username',
        'email': 'unique@example.com',
        'password': 'TestPass123!',
        'confirm_password': 'TestPass123!',
        'full_name': 'Test User'
    }
    user_data[field] = value  # Override with duplicate value
    
    # Act
    response = client.post(
        '/auth/register',
        data=user_data,
        follow_redirects=True
    )
    
    # Assert
    assert response.status_code == 200, "Form should be re-rendered with error"
    assert error_message in response.data, "Duplicate field error message not found"

def test_logout_requires_login(client: FlaskClient) -> None:
    """Test that logout requires the user to be logged in."""
    # Act - Try to logout when not logged in
    response = client.get('/auth/logout', follow_redirects=True)
    
    # Assert - Should redirect to login page
    assert response.status_code == 200
    assert b'Please log in to access this page' in response.data


def test_logout_success(auth_client: FlaskClient) -> None:
    """Test that a logged-in user can successfully log out."""
    # Act
    response = auth_client.get('/auth/logout', follow_redirects=True)
    
    # Assert
    assert response.status_code == 200
    assert b'You have been logged out' in response.data
    
    # Verify session is cleared
    with auth_client.session_transaction() as session:
        assert 'user_id' not in session, "User ID should be removed from session"

@pytest.mark.parametrize('username,password,expected_message', [
    # Non-existent user
    ('nonexistent', 'password', b'Invalid username or password'),
    # Wrong password
    ('testuser', 'wrongpass', b'Invalid username or password'),
    # Empty username
    ('', 'password', b'This field is required'),
    # Empty password
    ('testuser', '', b'This field is required'),
    # Inactive user (tested separately below)
])
def test_login_invalid_credentials(
    client: FlaskClient, 
    test_user: User,
    username: str, 
    password: str, 
    expected_message: bytes
) -> None:
    """Test login with various invalid credentials."""
    # Act
    response = client.post(
        '/auth/login',
        data={'username': username, 'password': password},
        follow_redirects=True
    )
    
    # Assert
    assert response.status_code == 200, "Form should be re-rendered with errors"
    assert expected_message in response.data, "Expected error message not found"


def test_login_inactive_user(client: FlaskClient, test_user: User) -> None:
    """Test that login fails for inactive users."""
    # Arrange - deactivate the test user
    test_user.is_active = False
    db.session.commit()
    
    # Act
    response = client.post(
        '/auth/login',
        data={'username': 'testuser', 'password': 'testpass123'},
        follow_redirects=True
    )
    
    # Assert
    assert response.status_code == 200
    assert b'Your account has been deactivated' in response.data

def test_password_reset_flow(client: FlaskClient, test_user: User) -> None:
    """Test the complete password reset flow (request + reset)."""
    # Step 1: Request password reset
    response = client.post(
        '/auth/forgot-password',
        data={'email': 'test@example.com'},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b'Password reset instructions have been sent' in response.data
    
    # In a real test, we'd extract the reset token from the email
    # For this test, we'll simulate getting a valid token
    token = test_user.get_reset_password_token()
    
    # Step 2: Reset password with the token
    new_password = 'NewSecurePass123!'
    response = client.post(
        f'/auth/reset-password/{token}',
        data={
            'password': new_password,
            'confirm_password': new_password
        },
        follow_redirects=True
    )
    
    # Verify success
    assert response.status_code == 200
    assert b'Your password has been reset' in response.data
    
    # Verify new password works
    response = client.post(
        '/auth/login',
        data={'username': 'testuser', 'password': new_password},
        follow_redirects=True
    )
    assert b'Logged in successfully' in response.data

def test_password_reset_invalid_token(client: FlaskClient) -> None:
    """Test password reset with an invalid or expired token."""
    # Act - Try to reset with an invalid token
    response = client.post(
        '/auth/reset-password/invalid-token-123',
        data={
            'password': 'NewPass123!',
            'confirm_password': 'NewPass123!'
        },
        follow_redirects=True
    )
    
    # Assert
    assert response.status_code == 200
    assert b'Invalid or expired password reset link' in response.data


def test_password_reset_expired_token(
    client: FlaskClient, 
    test_user: User,
    monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test password reset with an expired token."""
    # Arrange - make token expire immediately
    import time
    from app import app
    
    original_ts = app.config['RESET_TOKEN_EXPIRATION']
    app.config['RESET_TOKEN_EXPIRATION'] = -1  # Expired token
    
    # Get a token that will be expired
    token = test_user.get_reset_password_token()
    
    # Reset config
    app.config['RESET_TOKEN_EXPIRATION'] = original_ts
    
    # Act - Try to use the expired token
    response = client.post(
        f'/auth/reset-password/{token}',
        data={
            'password': 'NewPass123!',
            'confirm_password': 'NewPass123!'
        },
        follow_redirects=True
    )
    
    # Assert
    assert response.status_code == 200
    assert b'Invalid or expired password reset link' in response.data

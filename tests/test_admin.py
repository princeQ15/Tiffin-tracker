"""Test admin routes and functionality."""
import pytest
from flask import url_for
from app.models.user import User

def test_admin_requires_login(client):
    """Test that admin routes require login."""
    response = client.get('/admin', follow_redirects=True)
    assert b'Please log in to access this page' in response.data

def test_admin_requires_admin_role(auth_client):
    """Test that admin routes require admin role."""
    # Regular users should not be able to access admin
    response = auth_client.get('/admin', follow_redirects=True)
    assert response.status_code == 403  # Forbidden

@pytest.mark.skip(reason="Requires admin user setup")
def test_admin_dashboard(admin_client):
    """Test that admin dashboard is accessible to admin users."""
    response = admin_client.get('/admin')
    assert response.status_code == 200
    assert b'Admin Dashboard' in response.data

def test_admin_user_management(admin_client, db):
    """Test user management in admin panel."""
    # Test listing users
    response = admin_client.get('/admin/users')
    assert response.status_code == 200
    assert b'Users' in response.data
    
    # Test creating a new user
    response = admin_client.post('/admin/user/new', data={
        'username': 'newadmin',
        'email': 'newadmin@example.com',
        'password': 'adminpass123',
        'is_admin': True
    }, follow_redirects=True)
    
    assert b'User created successfully' in response.data
    
    # Verify user was created
    user = User.query.filter_by(email='newadmin@example.com').first()
    assert user is not None
    assert user.is_admin is True

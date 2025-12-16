"""Test cases for the Tiffin Tracker application."""

def test_app_creation(app):
    """Test that the app is created with the correct configuration."""
    assert app is not None
    assert app.config['TESTING'] is True
    assert app.config['WTF_CSRF_ENABLED'] is False

def test_home_page(client):
    """Test that the home page loads successfully."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Tiffin Tracker' in response.data

def test_404_page(client):
    """Test that 404 error page is returned for non-existent routes."""
    response = client.get('/non-existent-route')
    assert response.status_code == 404
    assert b'Not Found' in response.data

def test_static_files(client):
    """Test that static files are served correctly."""
    response = client.get('/static/css/style.css')
    assert response.status_code == 200
    assert response.content_type == 'text/css; charset=utf-8'

def test_login_page(client):
    """Test that the login page loads successfully."""
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'username' in response.data.lower()
    assert b'password' in response.data.lower()

def test_valid_login(client):
    """Test that a user can log in with valid credentials."""
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Logout' in response.data

def test_invalid_login(client):
    """Test that invalid login fails."""
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'wrongpassword'
    }, follow_redirects=True)
    assert b'Invalid username or password' in response.data

def test_protected_route_unauthorized(client):
    """Test that protected routes redirect to login when not authenticated."""
    response = client.get('/profile', follow_redirects=True)
    assert b'Please log in to access this page' in response.data

def test_protected_route_authorized(auth_client):
    """Test that protected routes are accessible when authenticated."""
    response = auth_client.get('/profile')
    assert response.status_code == 200
    assert b'Profile' in response.data

def test_logout(auth_client):
    """Test that a user can log out."""
    response = auth_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'You have been logged out' in response.data

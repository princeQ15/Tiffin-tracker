def test_app_creation(app):
    """Test that the app is created with the correct config."""
    assert app is not None
    assert app.config['TESTING'] is True

def test_home_page(client):
    """Test that the home page loads successfully."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Tiffin Tracker' in response.data

def test_login_page(client):
    """Test that the login page loads successfully."""
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'username' in response.data.lower()
    assert b'password' in response.data.lower()

# Test file: tests/test_app.py
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

def test_app_creation(client):
    assert client.get('/').status_code == 200

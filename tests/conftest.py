import os
import tempfile
import pytest
from app import create_app
from config import TestConfig

@pytest.fixture(scope='module')
def app():
    # Create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app(TestConfig)
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    # Create the database and load test data
    with app.app_context():
        from app.extensions import db
        db.create_all()
        
    yield app
    
    # Clean up the database file
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def db(app):
    from app.extensions import db
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()

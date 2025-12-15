# Test configuration
class TestConfig:
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SECRET_KEY = 'test-secret-key'

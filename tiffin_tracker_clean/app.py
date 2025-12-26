import os
from app import create_app, db
from app.models import User, Order

# Create the Flask application using the application factory
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Order=Order)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Blueprint

# Create auth blueprint
# The url_prefix will be added to all routes in this blueprint
auth = Blueprint('auth', __name__)

# Import views at the bottom to avoid circular imports
from . import views

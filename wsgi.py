import sys
import os

# The directory containing your application
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.append(path)

# Import the Flask app instance
from app import app as application  # noqa

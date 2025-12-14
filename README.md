# Tiffin Tracker

A web application for managing tiffin orders with order status updates and basic admin functionality.

## Features

- **User Authentication**
  - User registration and login/logout
  - Admin dashboard for managing orders
  - Password hashing using Werkzeug's security utilities
  - Session-based authentication using Flask's session

- **Order Management**
  - Place new tiffin orders
  - View order status updates
  - Order history for users
  - Basic order status management

- **Admin Features**
  - View all user orders
  - Update order status
  - Basic user management

- **Responsive Design**
  - Mobile-friendly layout
  - Clean and simple interface

## Tech Stack

- **Backend**: Python 3.8+, Flask
- **Frontend**: HTML5, JavaScript, Tailwind CSS
- **Database**: SQLite (file-based)
- **Authentication**: Flask's session management
- **Styling**: Tailwind CSS with custom components
- **Deployment**: Flask's built-in development server

## Project Structure

```text
tiffin-tracker/
├── app/                  # Application package
│   ├── __init__.py      # Application factory
│   ├── models/          # Database models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── order.py
│   │   └── meal.py
│   └── routes/          # Application routes
│       ├── __init__.py
│       ├── auth.py      # Authentication routes
│       └── main.py      # Main application routes
├── static/              # Static files
│   └── css/
│       └── style.css    # Custom styles
├── templates/           # HTML templates
│   ├── base.html        # Base template
│   ├── index.html       # Home page
│   ├── login.html       # Login page
│   ├── register.html    # Registration page
│   ├── profile.html     # User profile
│   └── admin.html       # Admin dashboard
├── app.py               # Main application entry point
├── config.py            # Configuration settings
├── db_utils.py          # Database helper functions
├── requirements.txt     # Python dependencies
└── schema.sql           # Database schema
```

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/TusharQ15/Tiffin-tracker.git
   cd Tiffin-tracker
   ```

2. **Create and activate a virtual environment**:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**:
   ```bash
   python -c "from app import create_app; create_app().app_context().push(); from app import db; db.create_all()"
   ```

5. **Run the application**:
   ```bash
   flask run
   ```
   The application will be available at `http://localhost:5000`

### Development Credentials

**⚠️ WARNING: For development use only!**

```
Default admin (development only):
- Username: admin
- Password: admin123
```

**Important:** Change these credentials immediately after first login in production environments.

## Screenshots

### Login Page
![Login Page](screenshots/login.png)

### User Dashboard
![User Dashboard](screenshots/dashboard.png)

### Admin Panel
![Admin Panel](screenshots/admin.png)
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   python init_db.py
   ```

## Running the Application

### Development Mode
```bash
# Set environment variables
set FLASK_APP=app.py
set FLASK_ENV=development

# Run the application
flask run
```

### Production Mode
```bash
# Using Waitress
waitress-serve --port=5000 app:app
```

## Default Admin Credentials

- **Username**: admin
- **Password**: admin123

## Project Structure

```
tiffin-tracker/
├── app.py                # Main application
├── requirements.txt      # Python dependencies
├── static/              # Static files (CSS, JS, images)
│   └── css/
│       └── style.css
├── templates/           # HTML templates
│   ├── base.html        # Base template
│   ├── index.html       # Home page
│   ├── login.html       # Login page
│   └── register.html    # Registration page
└── tiffin_orders.db     # SQLite database file
```

## Security

- Password hashing with PBKDF2
- CSRF protection
- Rate limiting on authentication endpoints
- Secure session management

## License

MIT License - See [LICENSE](LICENSE) for details.

## Support

For support, please open an issue in the GitHub repository.

# Tiffin Tracker

A web application for managing tiffin (meal) orders with user authentication and admin dashboard.

## Features

- User registration and authentication
- Place and track tiffin orders
- Admin dashboard for order management
- Responsive design with Tailwind CSS
- Secure password hashing
- Rate limiting for API endpoints
- CSRF protection
- SQLite database

## Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **Database**: SQLite
- **Authentication**: Session-based
- **Deployment**: Waitress (production WSGI server)

## Prerequisites

- Python 3.8+
- pip (Python package manager)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/tiffin-tracker.git
   cd tiffin-tracker
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   python -c "from app import init_db; init_db()"
   ```

## Running the Application

### Development
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

### Production
```bash
# Using Waitress
waitress-serve --port=5000 app:app
```

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
SECRET_KEY=your-secret-key-here
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123  # Change this in production
```

## Default Admin Credentials

- **Username**: admin
- **Password**: admin123

## Project Structure

```
tiffin-tracker/
├── app.py                # Main application
├── requirements.txt      # Python dependencies
├── schema.sql           # Database schema
├── static/              # Static files (CSS, JS, images)
│   └── css/
│       └── style.css
├── templates/           # HTML templates
│   ├── base.html        # Base template
│   ├── index.html       # Home page
│   ├── login.html       # Login page
│   ├── register.html    # Registration page
│   ├── admin.html       # Admin dashboard
│   └── error.html       # Error pages
└── tiffin_orders.db     # SQLite database (created on first run)
```

## Security Considerations

- All passwords are hashed using PBKDF2 with SHA-256
- CSRF protection is enabled
- Rate limiting on authentication endpoints
- Secure session configuration
- Input validation and sanitization

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

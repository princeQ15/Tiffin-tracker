"""Database utility functions for the Tiffin Tracker application.

This module provides helper functions for database operations including user management,
order management, and authentication decorators. It uses SQLite as the database backend.
"""

import sqlite3
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from flask import Flask, g, session, redirect, url_for, flash, Response
from werkzeug.security import generate_password_hash, check_password_hash

# Type aliases
SQLiteRow = sqlite3.Row
SQLiteCursor = sqlite3.Cursor
SQLiteConnection = sqlite3.Connection

def get_db() -> SQLiteConnection:
    """Get a database connection with row factory.
    
    This function uses Flask's application context to store the database connection
    so it can be reused within the same request.
    
    Returns:
        SQLiteConnection: A connection to the SQLite database with row factory set.
    """
    if 'db' not in g:
        g.db = sqlite3.connect('tiffin_orders.db')
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e: Optional[Exception] = None) -> None:
    """Close the database connection if it exists.
    
    This function is typically registered as a teardown_appcontext handler.
    
    Args:
        e: Optional exception that was raised during request handling, if any.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()

def query_db(
    query: str, 
    args: Tuple[Any, ...] = (), 
    one: bool = False
) -> Union[List[sqlite3.Row], sqlite3.Row, None]:
    """Execute a query and return the results.
    
    Args:
        query: SQL query string with placeholders.
        args: Tuple of values to substitute into the query placeholders.
        one: If True, return only the first result (or None).
        
    Returns:
        Union[List[sqlite3.Row], sqlite3.Row, None]: 
            - If one=True: A single row or None if no results.
            - If one=False: A list of rows (possibly empty).
    """
    db = get_db()
    cur = db.execute(query, args)
    rv = cur.fetchall()
    db.commit()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def get_user(user_id: int) -> Optional[sqlite3.Row]:
    """Get a user by their ID.
    
    Args:
        user_id: The ID of the user to retrieve.
        
    Returns:
        Optional[sqlite3.Row]: The user record if found, None otherwise.
    """
    return query_db('SELECT * FROM users WHERE id = ?', (user_id,), one=True)

def get_user_by_username(username: str) -> Optional[sqlite3.Row]:
    """Get a user by their username.
    
    Args:
        username: The username to search for.
        
    Returns:
        Optional[sqlite3.Row]: The user record if found, None otherwise.
    """
    return query_db('SELECT * FROM users WHERE username = ?', (username,), one=True)

def create_user(
    username: str, 
    password: str, 
    email: Optional[str] = None, 
    is_admin: bool = False
) -> Optional[sqlite3.Row]:
    """Create a new user in the database.
    
    Args:
        username: The username for the new user.
        password: The plain text password (will be hashed).
        email: Optional email address for the user.
        is_admin: Whether the user should have admin privileges.
        
    Returns:
        Optional[sqlite3.Row]: The created user record if successful, None otherwise.
        
    Note:
        The password will be hashed before being stored in the database.
    """
    try:
        hashed_pw = generate_password_hash(password)
        query_db(
            'INSERT INTO users (username, password, email, is_admin) VALUES (?, ?, ?, ?)',
            (username, hashed_pw, email, 1 if is_admin else 0)
        )
        return get_user_by_username(username)
    except sqlite3.IntegrityError as e:
        # Handle duplicate username/email
        if 'UNIQUE constraint failed: users.username' in str(e):
            raise ValueError(f"Username '{username}' is already taken.")
        elif 'UNIQUE constraint failed: users.email' in str(e):
            raise ValueError(f"Email '{email}' is already registered.")
        raise

def get_orders(user_id: Optional[int] = None) -> List[sqlite3.Row]:
    """Get orders from the database.
    
    Args:
        user_id: If provided, only return orders for this user.
        
    Returns:
        List[sqlite3.Row]: A list of order records, ordered by creation date (newest first).
    """
    if user_id is not None:
        return query_db(
            'SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC', 
            (user_id,)
        )
    return query_db('SELECT * FROM orders ORDER BY created_at DESC')

def get_order(order_id: int) -> Optional[sqlite3.Row]:
    """Get a specific order by its ID.
    
    Args:
        order_id: The ID of the order to retrieve.
        
    Returns:
        Optional[sqlite3.Row]: The order record if found, None otherwise.
    """
    return query_db('SELECT * FROM orders WHERE id = ?', (order_id,), one=True)

def create_order(
    user_id: int,
    name: str,
    phone: str,
    address: str,
    meal: str,
    quantity: int,
    delivery_time: str
) -> Optional[sqlite3.Row]:
    """Create a new order in the database.
    
    Args:
        user_id: The ID of the user placing the order.
        name: Name of the person placing the order.
        phone: Contact phone number.
        address: Delivery address.
        meal: The meal being ordered.
        quantity: Number of meals.
        delivery_time: Requested delivery time.
        
    Returns:
        Optional[sqlite3.Row]: The created order record if successful, None otherwise.
    """
    try:
        query_db(
            '''INSERT INTO orders 
               (user_id, name, phone, address, meal, quantity, delivery_time, status) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (user_id, name, phone, address, meal, quantity, delivery_time, 'Received')
        )
        # Get the ID of the newly created order
        result = query_db('SELECT last_insert_rowid()', one=True)
        if result and len(result) > 0:
            return get_order(result[0])
        return None
    except sqlite3.Error as e:
        print(f"Error creating order: {e}")
        return None

def update_order_status(order_id: int, status: str) -> bool:
    """Update order status"""
    query_db('UPDATE orders SET status = ? WHERE id = ?', (status, order_id))
    return True

def init_db() -> None:
    """Initialize the database with required tables.
    
    This function reads the schema from schema.sql and executes it to create
    the necessary tables if they don't already exist.
    
    Note:
        This should typically only be called once during application setup.
    """
    try:
        with get_db() as conn:
            with open('schema.sql', 'r') as f:
                conn.executescript(f.read())
            conn.commit()
    except FileNotFoundError:
        print("Error: schema.sql file not found.")
        raise
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")
        raise

# Authentication decorators
def login_required(f: Callable) -> Callable:
    """Decorator to ensure a user is logged in.
    
    Args:
        f: The view function to decorate.
        
    Returns:
        Callable: The decorated function that checks for authentication.
        
    Note:
        If the user is not logged in, they will be redirected to the login page.
    """
    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f: Callable) -> Callable:
    """Decorator to ensure a user is logged in and has admin privileges.
    
    Args:
        f: The view function to decorate.
        
    Returns:
        Callable: The decorated function that checks for admin status.
        
    Note:
        If the user is not logged in, they will be redirected to the login page.
        If the user is not an admin, they will be redirected to the home page.
    """
    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))
            
        user = get_user(session['user_id'])
        if not user or not user['is_admin']:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('index'))
            
        return f(*args, **kwargs)
    return decorated_function

-- Drop existing tables if they exist
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS users;

-- Create orders table
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    meal TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    date TEXT NOT NULL,
    status TEXT DEFAULT 'Order Placed',
    ip_address TEXT,
    delivery_address TEXT NOT NULL,
    delivery_time TEXT,
    estimated_delivery TEXT,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id),
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Create users table for future authentication
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    email TEXT UNIQUE,
    is_admin BOOLEAN DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    last_login TEXT
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(date);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);

-- Insert default admin user (password will be hashed by the application)
-- Default password is 'admin123' - CHANGE THIS IN PRODUCTION
INSERT OR IGNORE INTO users (username, password_hash, is_admin)
VALUES ('admin', 'pbkdf2:sha256:600000$your_salt_here$hashed_password_here', 1);

-- Create a trigger to update the updated_at timestamp
CREATE TRIGGER IF NOT EXISTS update_order_timestamp
AFTER UPDATE ON orders
FOR EACH ROW
BEGIN
    UPDATE orders SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
END;

import sqlite3
from datetime import datetime
import hashlib
import os

DATABASE = 'database.db'

def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with users and expenses tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create expenses table with user_id
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date DATE NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")

class User:
    """User model for authentication"""
    
    @staticmethod
    def hash_password(password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def create(username, email, password):
        """Create a new user"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            hashed_password = User.hash_password(password)
            cursor.execute('''
                INSERT INTO users (username, email, password)
                VALUES (?, ?, ?)
            ''', (username, email, hashed_password))
            
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return user_id
        except sqlite3.IntegrityError:
            conn.close()
            return None
    
    @staticmethod
    def authenticate(username, password):
        """Authenticate user with username and password"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        hashed_password = User.hash_password(password)
        cursor.execute('''
            SELECT * FROM users WHERE username = ? AND password = ?
        ''', (username, hashed_password))
        
        user = cursor.fetchone()
        conn.close()
        
        return dict(user) if user else None
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        
        return dict(user) if user else None

class Expense:
    """Expense model for handling expense data"""
    
    @staticmethod
    def create(user_id, date, category, description, amount):
        """Create a new expense for a user"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO expenses (user_id, date, category, description, amount)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, date, category, description, amount))
        
        conn.commit()
        expense_id = cursor.lastrowid
        conn.close()
        
        return expense_id
    
    @staticmethod
    def get_all(user_id):
        """Get all expenses for a user ordered by date"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM expenses
            WHERE user_id = ?
            ORDER BY date DESC, id DESC
        ''', (user_id,))
        
        expenses = cursor.fetchall()
        conn.close()
        
        return [dict(expense) for expense in expenses]
    
    @staticmethod
    def get_by_id(expense_id, user_id):
        """Get a single expense by ID for a user"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM expenses WHERE id = ? AND user_id = ?', (expense_id, user_id))
        expense = cursor.fetchone()
        conn.close()
        
        return dict(expense) if expense else None
    
    @staticmethod
    def delete(expense_id, user_id):
        """Delete an expense by ID for a user"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM expenses WHERE id = ? AND user_id = ?', (expense_id, user_id))
        conn.commit()
        deleted = cursor.rowcount > 0
        conn.close()
        
        return deleted
    
    @staticmethod
    def get_monthly_summary(user_id):
        """Get monthly expense summary for a user"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                strftime('%Y', date) as year,
                strftime('%m', date) as month,
                SUM(amount) as total
            FROM expenses
            WHERE user_id = ?
            GROUP BY year, month
            ORDER BY year, month
        ''', (user_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        summary = []
        for row in results:
            year = row['year']
            month = row['month']
            total = row['total']
            
            month_name = datetime(int(year), int(month), 1).strftime('%B %Y')
            summary.append({
                'month': month_name,
                'total': round(total, 2)
            })
        
        return summary
    
    @staticmethod
    def get_category_summary(user_id):
        """Get category-wise expense summary for a user"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                category,
                COUNT(*) as count,
                SUM(amount) as total
            FROM expenses
            WHERE user_id = ?
            GROUP BY category
            ORDER BY total DESC
        ''', (user_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [{
            'category': row['category'],
            'count': row['count'],
            'total': round(row['total'], 2)
        } for row in results]
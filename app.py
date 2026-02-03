from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from models import Expense, User, init_db
from datetime import datetime
from functools import wraps

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'  # Change this!

# Initialize database
init_db()

# ==================== AUTHENTICATION DECORATOR ====================

def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== AUTHENTICATION ROUTES ====================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        user = User.authenticate(username, password)
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return jsonify({'success': True, 'message': 'Login successful'}), 200
        else:
            return jsonify({'success': False, 'error': 'Invalid username or password'}), 401
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register page"""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        # Validate input
        if not username or not email or not password:
            return jsonify({'success': False, 'error': 'All fields are required'}), 400
        
        if len(password) < 6:
            return jsonify({'success': False, 'error': 'Password must be at least 6 characters'}), 400
        
        user_id = User.create(username, email, password)
        
        if user_id:
            return jsonify({'success': True, 'message': 'Registration successful! Please login.'}), 201
        else:
            return jsonify({'success': False, 'error': 'Username or email already exists'}), 400
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    return redirect(url_for('login'))

# ==================== MAIN ROUTES ====================

@app.route('/')
@login_required
def index():
    """Render main page"""
    return render_template('index.html', username=session.get('username'))

@app.route('/summary')
@login_required
def summary():
    """Render summary page"""
    return render_template('summary.html', username=session.get('username'))

# ==================== API ENDPOINTS ====================

@app.route('/add-expense', methods=['POST'])
@login_required
def add_expense():
    """Add new expense to database"""
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['date', 'category', 'description', 'amount']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        try:
            datetime.strptime(data['date'], '%Y-%m-%d')
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        try:
            amount = float(data['amount'])
            if amount <= 0:
                return jsonify({'error': 'Amount must be greater than 0'}), 400
        except ValueError:
            return jsonify({'error': 'Invalid amount format'}), 400
        
        expense_id = Expense.create(
            user_id=session['user_id'],
            date=data['date'],
            category=data['category'],
            description=data['description'],
            amount=amount
        )
        
        new_expense = Expense.get_by_id(expense_id, session['user_id'])
        
        return jsonify({
            'message': 'Expense added successfully',
            'expense': new_expense
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/expenses', methods=['GET'])
@login_required
def get_expenses():
    """Get all expenses for logged-in user"""
    try:
        expenses = Expense.get_all(session['user_id'])
        return jsonify({
            'expenses': expenses,
            'total': len(expenses)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/monthly-summary', methods=['GET'])
@login_required
def monthly_summary():
    """Get monthly expense summary"""
    try:
        summary = Expense.get_monthly_summary(session['user_id'])
        return jsonify({
            'summary': summary
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/category-summary', methods=['GET'])
@login_required
def category_summary():
    """Get category-wise expense summary"""
    try:
        summary = Expense.get_category_summary(session['user_id'])
        return jsonify({
            'summary': summary
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete-expense/<int:expense_id>', methods=['DELETE'])
@login_required
def delete_expense(expense_id):
    """Delete an expense"""
    try:
        deleted = Expense.delete(expense_id, session['user_id'])
        
        if not deleted:
            return jsonify({'error': 'Expense not found'}), 404
        
        return jsonify({'message': 'Expense deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# ==================== RUN APP ====================

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 Personal Expense Tracker with Authentication")
    print("="*50)
    print("📍 Running on: http://127.0.0.1:5000")
    print("📝 Press CTRL+C to quit")
    print("="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
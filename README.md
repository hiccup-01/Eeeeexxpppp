# 💰 Personal Expense Tracker (with Authentication & Charts)

A feature-rich Flask web application for tracking personal expenses with user authentication, interactive charts, and detailed analytics.

**✨ Python 3.14.2 Compatible!** This version uses native SQLite3 instead of SQLAlchemy for full compatibility with the latest Python version.

**🆕 New Features:** User login system, beautiful charts (Bar & Line), and multi-user support!

## 📋 Features

- ✅ **User Authentication** - Secure login and registration system
- ✅ **Add daily expenses** with date, category, description, and amount
- ✅ **View all expenses** in a dynamic table
- ✅ **Delete expenses** with confirmation
- ✅ **Monthly expense summary** with totals
- ✅ **Category-wise expense analysis** with percentages
- ✅ **Interactive Charts** - Bar charts and line graphs for visual analytics
- ✅ **Responsive design** - Works on desktop and mobile
- ✅ **Multi-user support** - Each user has their own expenses

## 🛠️ Tech Stack

- **Backend:** Python 3.14.2, Flask, Sessions
- **Frontend:** HTML5, CSS3, JavaScript (Fetch API), Chart.js
- **Database:** SQLite3 (built-in)
- **Authentication:** Password hashing with SHA-256

## 📁 Project Structure

```
expense_tracker/
│
├── app.py                  # Main Flask application with auth
├── models.py               # Database models (User & Expense)
├── database.db             # SQLite database (auto-generated)
├── requirements.txt        # Python dependencies
├── README.md              # This file
│
├── templates/
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   ├── index.html         # Main page (add expenses)
│   └── summary.html       # Summary page with charts
│
└── static/
    ├── css/
    │   └── style.css      # Stylesheet (includes auth styles)
    └── js/
        └── script.js      # JavaScript for API calls
```

## 🚀 Setup Instructions

### Prerequisites

- Python 3.14.2 (or Python 3.8+)
- pip (Python package manager)

**Note:** This version uses native SQLite3 (built into Python) instead of SQLAlchemy, making it fully compatible with Python 3.14.2!

### Step 1: Clone or Download the Project

Download all project files and organize them according to the folder structure above.

### Step 2: Create Virtual Environment (Optional but Recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

**IMPORTANT:** Before running, change the secret key in `app.py`:
```python
app.secret_key = 'your-unique-secret-key-here'  # Change this!
```

Then run:
```bash
python app.py
```

The application will start on `http://127.0.0.1:5000/`

### Step 5: Open in Browser

Navigate to `http://127.0.0.1:5000/` in your web browser.

## 📖 How to Use

### First Time Setup

1. **Register a New Account:**
   - Go to `http://127.0.0.1:5000/register`
   - Enter username, email, and password (min 6 characters)
   - Click "Register"
   - You'll be redirected to login

2. **Login:**
   - Go to `http://127.0.0.1:5000/login`
   - Enter your username and password
   - Click "Login"

### Adding an Expense

1. After logging in, you'll see the main page
2. Fill in the form:
   - **Date:** Select the expense date
   - **Category:** Choose from predefined categories
   - **Description:** Brief description of the expense
   - **Amount:** Enter the amount in dollars
3. Click "Add Expense"
4. The expense will appear in the table below

### Viewing Summary & Charts

1. Click on "View Summary" in the navigation
2. See beautiful visualizations:
   - **Bar Chart:** Shows expenses by category
   - **Line Chart:** Shows monthly spending trends
   - **Monthly Cards:** Total spending per month
   - **Category Table:** Detailed breakdown with percentages

### Deleting an Expense

1. In the Recent Expenses table, click the "Delete" button
2. Confirm the deletion
3. The expense will be removed

### Logout

Click the "Logout" button in the header to end your session

## 🔌 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/register` | Register new user |
| GET/POST | `/login` | Login user |
| GET | `/logout` | Logout user |

### Expenses (Requires Login)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/add-expense` | Add a new expense |
| GET | `/expenses` | Get all expenses for logged-in user |
| GET | `/monthly-summary` | Get monthly totals |
| GET | `/category-summary` | Get category-wise totals |
| DELETE | `/delete-expense/<id>` | Delete an expense by ID |

## 💡 Learning Outcomes

## 💡 Learning Outcomes

By completing this project, students will learn:

- ✅ Flask routing and request handling
- ✅ RESTful API design
- ✅ Database operations (CRUD) using SQLite3
- ✅ **User authentication and session management**
- ✅ **Password hashing for security**
- ✅ **Multi-user data isolation**
- ✅ Raw SQL queries with foreign keys
- ✅ Frontend-backend communication using Fetch API
- ✅ Form validation (client and server-side)
- ✅ Date handling in Python
- ✅ SQL aggregation functions (SUM, GROUP BY)
- ✅ JSON data exchange
- ✅ Error handling in Flask
- ✅ **Data visualization with Chart.js**
- ✅ **Creating interactive bar and line charts**

## 🎨 Customization Ideas

1. ~~**Add user authentication**~~ ✅ DONE!
2. **Add edit functionality** - Update existing expenses
3. **Export to Excel/CSV** - Download expenses
4. ~~**Add charts**~~ ✅ DONE!
5. **Budget tracking** - Set monthly budgets and track progress
6. **Recurring expenses** - Auto-add regular expenses
7. **Search and filter** - Find expenses by date range or category
8. **Email notifications** - Get spending alerts
9. **Receipt upload** - Attach receipt images
10. **Pie charts** - Additional visualization options

## 🗄️ Database Structure

The application uses two tables:

### Users Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| username | TEXT | Unique username |
| email | TEXT | Unique email |
| password | TEXT | Hashed password (SHA-256) |
| created_at | TIMESTAMP | Registration date |

### Expenses Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| user_id | INTEGER | Foreign key to users table |
| date | DATE | Expense date |
| category | TEXT | Expense category |
| description | TEXT | Expense description |
| amount | REAL | Expense amount |

## ❗ Common Issues

### Database not created

Make sure Flask is properly initialized. The database will be created automatically when you run the app for the first time.

### Port already in use

If port 5000 is already in use, change it in `app.py`:
```python
app.run(debug=True, port=5001)  # Use different port
```

### Module not found errors

Make sure you've installed Flask:
```bash
pip install Flask==3.1.0
```

Or install from requirements.txt:
```bash
pip install -r requirements.txt
```

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Fetch API Guide](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)

## 📝 License

This project is for educational purposes. Feel free to use and modify as needed.

## 🤝 Contributing

This is a beginner project. Students are encouraged to:
- Add new features
- Improve the UI/UX
- Optimize the code
- Fix bugs

---

**Happy Coding! 🚀**# 💰 Personal Expense Tracker (with Authentication & Charts)

A feature-rich Flask web application for tracking personal expenses with user authentication, interactive charts, and detailed analytics.

**✨ Python 3.14.2 Compatible!** This version uses native SQLite3 instead of SQLAlchemy for full compatibility with the latest Python version.

**🆕 New Features:** User login system, beautiful charts (Bar & Line), and multi-user support!

## 📋 Features

- ✅ **User Authentication** - Secure login and registration system
- ✅ **Add daily expenses** with date, category, description, and amount
- ✅ **View all expenses** in a dynamic table
- ✅ **Delete expenses** with confirmation
- ✅ **Monthly expense summary** with totals
- ✅ **Category-wise expense analysis** with percentages
- ✅ **Interactive Charts** - Bar charts and line graphs for visual analytics
- ✅ **Responsive design** - Works on desktop and mobile
- ✅ **Multi-user support** - Each user has their own expenses

## 🛠️ Tech Stack

- **Backend:** Python 3.14.2, Flask, Sessions
- **Frontend:** HTML5, CSS3, JavaScript (Fetch API), Chart.js
- **Database:** SQLite3 (built-in)
- **Authentication:** Password hashing with SHA-256

## 📁 Project Structure

```
expense_tracker/
│
├── app.py                  # Main Flask application with auth
├── models.py               # Database models (User & Expense)
├── database.db             # SQLite database (auto-generated)
├── requirements.txt        # Python dependencies
├── README.md              # This file
│
├── templates/
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   ├── index.html         # Main page (add expenses)
│   └── summary.html       # Summary page with charts
│
└── static/
    ├── css/
    │   └── style.css      # Stylesheet (includes auth styles)
    └── js/
        └── script.js      # JavaScript for API calls
```

## 🚀 Setup Instructions

### Prerequisites

- Python 3.14.2 (or Python 3.8+)
- pip (Python package manager)

**Note:** This version uses native SQLite3 (built into Python) instead of SQLAlchemy, making it fully compatible with Python 3.14.2!

### Step 1: Clone or Download the Project

Download all project files and organize them according to the folder structure above.

### Step 2: Create Virtual Environment (Optional but Recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

**IMPORTANT:** Before running, change the secret key in `app.py`:
```python
app.secret_key = 'your-unique-secret-key-here'  # Change this!
```

Then run:
```bash
python app.py
```

The application will start on `http://127.0.0.1:5000/`

### Step 5: Open in Browser

Navigate to `http://127.0.0.1:5000/` in your web browser.

## 📖 How to Use

### First Time Setup

1. **Register a New Account:**
   - Go to `http://127.0.0.1:5000/register`
   - Enter username, email, and password (min 6 characters)
   - Click "Register"
   - You'll be redirected to login

2. **Login:**
   - Go to `http://127.0.0.1:5000/login`
   - Enter your username and password
   - Click "Login"

### Adding an Expense

1. After logging in, you'll see the main page
2. Fill in the form:
   - **Date:** Select the expense date
   - **Category:** Choose from predefined categories
   - **Description:** Brief description of the expense
   - **Amount:** Enter the amount in dollars
3. Click "Add Expense"
4. The expense will appear in the table below

### Viewing Summary & Charts

1. Click on "View Summary" in the navigation
2. See beautiful visualizations:
   - **Bar Chart:** Shows expenses by category
   - **Line Chart:** Shows monthly spending trends
   - **Monthly Cards:** Total spending per month
   - **Category Table:** Detailed breakdown with percentages

### Deleting an Expense

1. In the Recent Expenses table, click the "Delete" button
2. Confirm the deletion
3. The expense will be removed

### Logout

Click the "Logout" button in the header to end your session

## 🔌 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/register` | Register new user |
| GET/POST | `/login` | Login user |
| GET | `/logout` | Logout user |

### Expenses (Requires Login)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/add-expense` | Add a new expense |
| GET | `/expenses` | Get all expenses for logged-in user |
| GET | `/monthly-summary` | Get monthly totals |
| GET | `/category-summary` | Get category-wise totals |
| DELETE | `/delete-expense/<id>` | Delete an expense by ID |

## 💡 Learning Outcomes

## 💡 Learning Outcomes

By completing this project, students will learn:

- ✅ Flask routing and request handling
- ✅ RESTful API design
- ✅ Database operations (CRUD) using SQLite3
- ✅ **User authentication and session management**
- ✅ **Password hashing for security**
- ✅ **Multi-user data isolation**
- ✅ Raw SQL queries with foreign keys
- ✅ Frontend-backend communication using Fetch API
- ✅ Form validation (client and server-side)
- ✅ Date handling in Python
- ✅ SQL aggregation functions (SUM, GROUP BY)
- ✅ JSON data exchange
- ✅ Error handling in Flask
- ✅ **Data visualization with Chart.js**
- ✅ **Creating interactive bar and line charts**

## 🎨 Customization Ideas

1. ~~**Add user authentication**~~ ✅ DONE!
2. **Add edit functionality** - Update existing expenses
3. **Export to Excel/CSV** - Download expenses
4. ~~**Add charts**~~ ✅ DONE!
5. **Budget tracking** - Set monthly budgets and track progress
6. **Recurring expenses** - Auto-add regular expenses
7. **Search and filter** - Find expenses by date range or category
8. **Email notifications** - Get spending alerts
9. **Receipt upload** - Attach receipt images
10. **Pie charts** - Additional visualization options

## 🗄️ Database Structure

The application uses two tables:

### Users Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| username | TEXT | Unique username |
| email | TEXT | Unique email |
| password | TEXT | Hashed password (SHA-256) |
| created_at | TIMESTAMP | Registration date |

### Expenses Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| user_id | INTEGER | Foreign key to users table |
| date | DATE | Expense date |
| category | TEXT | Expense category |
| description | TEXT | Expense description |
| amount | REAL | Expense amount |

## ❗ Common Issues

### Database not created

Make sure Flask is properly initialized. The database will be created automatically when you run the app for the first time.

### Port already in use

If port 5000 is already in use, change it in `app.py`:
```python
app.run(debug=True, port=5001)  # Use different port
```

### Module not found errors

Make sure you've installed Flask:
```bash
pip install Flask==3.1.0
```

Or install from requirements.txt:
```bash
pip install -r requirements.txt
```

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Fetch API Guide](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)

## 📝 License

This project is for educational purposes. Feel free to use and modify as needed.

## 🤝 Contributing

This is a beginner project. Students are encouraged to:
- Add new features
- Improve the UI/UX
- Optimize the code
- Fix bugs

---

**Happy Coding! 🚀**
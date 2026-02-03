import sqlite3
from datetime import datetime

def check_database():
    """Check and display all expenses in the database"""
    
    try:
        # Connect to database
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='expenses'
        """)
        
        if not cursor.fetchone():
            print("❌ No 'expenses' table found. Run the Flask app first to create it.")
            return
        
        # Get all expenses
        cursor.execute('SELECT * FROM expenses ORDER BY date DESC')
        expenses = cursor.fetchall()
        
        if not expenses:
            print("\n📝 Database is empty. No expenses found.")
            print("   Add some expenses through the web app!\n")
            return
        
        # Display expenses
        print("\n" + "="*80)
        print(f"💰 EXPENSE DATABASE - Total Records: {len(expenses)}")
        print("="*80)
        print(f"{'ID':<5} {'Date':<12} {'Category':<15} {'Description':<25} {'Amount':>10}")
        print("-"*80)
        
        total = 0
        for expense in expenses:
            total += expense['amount']
            print(f"{expense['id']:<5} {expense['date']:<12} {expense['category']:<15} "
                  f"{expense['description']:<25} ${expense['amount']:>9.2f}")
        
        print("-"*80)
        print(f"{'TOTAL:':<57} ${total:>9.2f}")
        print("="*80 + "\n")
        
        # Show category summary
        cursor.execute("""
            SELECT category, COUNT(*) as count, SUM(amount) as total
            FROM expenses
            GROUP BY category
            ORDER BY total DESC
        """)
        
        categories = cursor.fetchall()
        
        print("\n📊 CATEGORY SUMMARY:")
        print("-"*50)
        print(f"{'Category':<20} {'Count':>10} {'Total':>15}")
        print("-"*50)
        
        for cat in categories:
            print(f"{cat['category']:<20} {cat['count']:>10} ${cat['total']:>14.2f}")
        
        print("-"*50 + "\n")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"❌ Database Error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    check_database()
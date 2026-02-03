// ==================== UTILITY FUNCTIONS ====================

// Display message to user
function showMessage(message, type = 'success') {
    const messageDiv = document.getElementById('message');
    if (messageDiv) {
        messageDiv.textContent = message;
        messageDiv.className = `message ${type}`;
        messageDiv.style.display = 'block';
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            messageDiv.style.display = 'none';
        }, 5000);
    }
}

// Format currency
function formatCurrency(amount) {
    return `$${parseFloat(amount).toFixed(2)}`;
}

// Set today's date as default
window.onload = function() {
    const dateInput = document.getElementById('date');
    if (dateInput) {
        const today = new Date().toISOString().split('T')[0];
        dateInput.value = today;
        
        // Load expenses on page load
        console.log('Page loaded, loading expenses...');
        loadExpenses();
    }
};

// ==================== ADD EXPENSE ====================

// Handle form submission
const expenseForm = document.getElementById('expenseForm');
if (expenseForm) {
    expenseForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        console.log('Form submitted');
        
        // Get form data
        const formData = {
            date: document.getElementById('date').value,
            category: document.getElementById('category').value,
            description: document.getElementById('description').value,
            amount: document.getElementById('amount').value
        };
        
        console.log('Form data:', formData);
        
        try {
            // Send POST request to backend
            console.log('Sending POST request to /add-expense');
            const response = await fetch('/add-expense', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });
            
            console.log('Response status:', response.status);
            const result = await response.json();
            console.log('Response data:', result);
            
            if (response.ok) {
                showMessage('Expense added successfully!', 'success');
                expenseForm.reset();
                
                // Reset date to today
                const today = new Date().toISOString().split('T')[0];
                document.getElementById('date').value = today;
                
                // Reload expenses table
                console.log('Reloading expenses...');
                loadExpenses();
            } else {
                showMessage(result.error || 'Failed to add expense', 'error');
                console.error('Error from server:', result);
            }
            
        } catch (error) {
            showMessage('Network error. Please try again.', 'error');
            console.error('Fetch error:', error);
        }
    });
}

// ==================== LOAD EXPENSES ====================

async function loadExpenses() {
    const tableBody = document.getElementById('expenseTableBody');
    
    if (!tableBody) {
        console.error('Table body element not found');
        return;
    }
    
    try {
        console.log('Starting to load expenses...');
        
        // Show loading state
        tableBody.innerHTML = '<tr><td colspan="5" class="loading">Loading expenses...</td></tr>';
        
        // Fetch expenses from backend
        console.log('Fetching from /expenses');
        const response = await fetch('/expenses');
        console.log('Response received, status:', response.status);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Data received:', data);
        
        if (data.expenses.length === 0) {
            console.log('No expenses found');
            tableBody.innerHTML = '<tr><td colspan="5" class="loading">No expenses found. Add your first expense!</td></tr>';
            const totalElement = document.getElementById('totalExpenses');
            if (totalElement) {
                totalElement.textContent = '$0.00';
            }
            return;
        }
        
        // Calculate total
        let total = 0;
        
        // Build table rows
        let html = '';
        data.expenses.forEach(expense => {
            total += parseFloat(expense.amount);
            html += `
                <tr>
                    <td>${expense.date}</td>
                    <td>${expense.category}</td>
                    <td>${expense.description}</td>
                    <td>${formatCurrency(expense.amount)}</td>
                    <td>
                        <button class="btn-delete" onclick="deleteExpense(${expense.id})">Delete</button>
                    </td>
                </tr>
            `;
        });
        
        console.log('Updating table with', data.expenses.length, 'expenses');
        tableBody.innerHTML = html;
        
        const totalElement = document.getElementById('totalExpenses');
        if (totalElement) {
            totalElement.textContent = formatCurrency(total);
        }
        
        console.log('Expenses loaded successfully');
        
    } catch (error) {
        console.error('Error loading expenses:', error);
        tableBody.innerHTML = `<tr><td colspan="5" class="loading">Error: ${error.message}. Check console for details.</td></tr>`;
        showMessage('Failed to load expenses. Check console for details.', 'error');
    }
}

// ==================== DELETE EXPENSE ====================

async function deleteExpense(expenseId) {
    console.log('Attempting to delete expense:', expenseId);
    
    if (!confirm('Are you sure you want to delete this expense?')) {
        return;
    }
    
    try {
        console.log('Sending DELETE request');
        const response = await fetch(`/delete-expense/${expenseId}`, {
            method: 'DELETE'
        });
        
        const result = await response.json();
        console.log('Delete response:', result);
        
        if (response.ok) {
            showMessage('Expense deleted successfully!', 'success');
            loadExpenses();
        } else {
            showMessage(result.error || 'Failed to delete expense', 'error');
        }
        
    } catch (error) {
        showMessage('Network error. Please try again.', 'error');
        console.error('Delete error:', error);
    }
}

// ==================== MONTHLY SUMMARY ====================

async function loadMonthlySummary() {
    const summaryDiv = document.getElementById('monthlySummary');
    
    if (!summaryDiv) {
        console.error('Monthly summary element not found');
        return;
    }
    
    try {
        console.log('Loading monthly summary...');
        summaryDiv.innerHTML = '<p class="loading">Loading monthly summary...</p>';
        
        const response = await fetch('/monthly-summary');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Monthly summary data:', data);
        
        if (data.summary.length === 0) {
            summaryDiv.innerHTML = '<p class="loading">No expenses recorded yet.</p>';
            return;
        }
        
        let html = '';
        data.summary.forEach(item => {
            html += `
                <div class="summary-card">
                    <h3>${item.month}</h3>
                    <div class="amount">${formatCurrency(item.total)}</div>
                </div>
            `;
        });
        
        summaryDiv.innerHTML = html;
        console.log('Monthly summary loaded successfully');
        
    } catch (error) {
        console.error('Error loading monthly summary:', error);
        summaryDiv.innerHTML = `<p class="loading">Error: ${error.message}</p>`;
    }
}

// ==================== CATEGORY SUMMARY ====================

async function loadCategorySummary() {
    const tableBody = document.getElementById('categoryTableBody');
    
    if (!tableBody) {
        console.error('Category table body not found');
        return;
    }
    
    try {
        console.log('Loading category summary...');
        tableBody.innerHTML = '<tr><td colspan="4" class="loading">Loading category summary...</td></tr>';
        
        const response = await fetch('/category-summary');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Category summary data:', data);
        
        if (data.summary.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="4" class="loading">No expenses recorded yet.</td></tr>';
            const grandTotalElement = document.getElementById('grandTotal');
            if (grandTotalElement) {
                grandTotalElement.textContent = '$0.00';
            }
            return;
        }
        
        let grandTotal = 0;
        let html = '';
        
        // Calculate grand total first
        data.summary.forEach(item => {
            grandTotal += parseFloat(item.total);
        });
        
        // Build table rows with percentages
        data.summary.forEach(item => {
            const percentage = ((parseFloat(item.total) / grandTotal) * 100).toFixed(1);
            html += `
                <tr>
                    <td>${item.category}</td>
                    <td>${item.count}</td>
                    <td>${formatCurrency(item.total)}</td>
                    <td>${percentage}%</td>
                </tr>
            `;
        });
        
        tableBody.innerHTML = html;
        
        const grandTotalElement = document.getElementById('grandTotal');
        if (grandTotalElement) {
            grandTotalElement.textContent = formatCurrency(grandTotal);
        }
        
        console.log('Category summary loaded successfully');
        
    } catch (error) {
        console.error('Error loading category summary:', error);
        tableBody.innerHTML = `<tr><td colspan="4" class="loading">Error: ${error.message}</td></tr>`;
    }
}
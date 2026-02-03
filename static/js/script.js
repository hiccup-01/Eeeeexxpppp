// ==================== UTILITY FUNCTIONS ====================

// Display message to user
function showMessage(message, type = 'success') {
    const messageDiv = document.getElementById('message');
    if (messageDiv) {
        messageDiv.textContent = message;
        messageDiv.className = `message ${type}`;
        messageDiv.style.display = 'block';
        
        // Auto-hide after 3 seconds
        setTimeout(() => {
            messageDiv.style.display = 'none';
        }, 3000);
    }
}

// Format currency
function formatCurrency(amount) {
    return `₹${parseFloat(amount).toFixed(2)}`;
}

// Set today's date and load data on startup
window.onload = function() {
    const dateInput = document.getElementById('date');
    if (dateInput) {
        const today = new Date().toISOString().split('T')[0];
        dateInput.value = today;
        loadExpenses(); // Load data from LocalStorage
    }
};

// ==================== MOCK DATABASE (LOCAL STORAGE) ====================
// Since GitHub Pages is static, we simulate a database using browser memory.

function getLocalExpenses() {
    const expenses = localStorage.getItem('expenses');
    return expenses ? JSON.parse(expenses) : [];
}

function saveLocalExpenses(expenses) {
    localStorage.setItem('expenses', JSON.stringify(expenses));
}

// ==================== ADD EXPENSE ====================

const expenseForm = document.getElementById('expenseForm');
if (expenseForm) {
    expenseForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        // Get form data
        const newExpense = {
            id: Date.now(), // Generate a unique ID based on time
            date: document.getElementById('date').value,
            category: document.getElementById('category').value,
            description: document.getElementById('description').value,
            amount: parseFloat(document.getElementById('amount').value)
        };
        
        // Save to LocalStorage (Simulating Database)
        const expenses = getLocalExpenses();
        expenses.unshift(newExpense); // Add to top of list
        saveLocalExpenses(expenses);

        // Success Feedback
        showMessage('Expense added! (Demo Mode)', 'success');
        expenseForm.reset();
        
        // Reset date
        const today = new Date().toISOString().split('T')[0];
        document.getElementById('date').value = today;
        
        // Reload table
        loadExpenses();
    });
}

// ==================== LOAD EXPENSES ====================

function loadExpenses() {
    const tableBody = document.getElementById('expenseTableBody');
    const totalElement = document.getElementById('totalExpenses');
    
    if (!tableBody) return;

    // Get data from LocalStorage
    const expenses = getLocalExpenses();
    
    // 1. Update Total
    const total = expenses.reduce((sum, item) => sum + item.amount, 0);
    if (totalElement) totalElement.textContent = formatCurrency(total);

    // 2. Update Table
    if (expenses.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="5" class="loading">No expenses yet. Add one to test!</td></tr>';
        return;
    }

    let html = '';
    expenses.forEach(expense => {
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
    
    tableBody.innerHTML = html;
}

// ==================== DELETE EXPENSE ====================

function deleteExpense(id) {
    if (!confirm('Delete this expense?')) return;

    let expenses = getLocalExpenses();
    expenses = expenses.filter(expense => expense.id !== id);
    saveLocalExpenses(expenses);

    showMessage('Expense deleted (Demo Mode)', 'success');
    loadExpenses();
}

// ==================== SUMMARY PAGE (OPTIONAL) ====================
// If you have a summary.html, this simple mock logic will load charts

function loadMonthlySummary() {
    console.log("Summary charts requires backend logic. In demo mode, this is static.");
}

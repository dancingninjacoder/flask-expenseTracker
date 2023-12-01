document.addEventListener('DOMContentLoaded', function() {
    const addExpenseForm = document.getElementById('addExpenseForm');
    const expensesTableBody = document.querySelector('#expensesTable tbody');
    const totalExpensesElement = document.getElementById('totalExpenses');
    let expenses = loadExpenses(); // Load expenses from local storage
    displayExpenses(expenses); // Display the loaded expenses

    addExpenseForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const expenseName = document.getElementById('expenseName').value;
        const expenseAmount = parseFloat(document.getElementById('expenseAmount').value);
        const expenseCategory = document.getElementById('expenseCategory').value;
        const currentDate = new Date().toISOString().split('T')[0];

        const newExpense = {
            date: currentDate,
            name: expenseName,
            amount: expenseAmount,
            category: expenseCategory
        };

        expenses.push(newExpense);
        saveExpenses(expenses);
        addExpenseToTable(newExpense);
        updateTotalExpenses();
        addExpenseForm.reset();
    });

    window.deleteExpense = function(index) {
        expenses.splice(index, 1);
        saveExpenses(expenses);
        displayExpenses(expenses);
        updateTotalExpenses();
    };

    function addExpenseToTable(expense) {
        const row = expensesTableBody.insertRow();
        row.innerHTML = `
            <td>${expense.date}</td>
            <td>${expense.name}</td>
            <td>${expense.amount.toFixed(2)}</td>
            <td>${expense.category}</td>
            <td><button onclick="deleteExpense(${expenses.indexOf(expense)})">Delete</button></td>
        `;
    }

    function displayExpenses(expenses) {
        expensesTableBody.innerHTML = ''; // Clear the table first
        expenses.forEach(expense => {
            addExpenseToTable(expense);
        });
        updateTotalExpenses();
    }

    function updateTotalExpenses() {
        const totalExpenses = expenses.reduce((acc, expense) => acc + expense.amount, 0);
        totalExpensesElement.innerText = totalExpenses.toFixed(2);
    }

    function saveExpenses(expenses) {
        localStorage.setItem('expenses', JSON.stringify(expenses));
    }

    function loadExpenses() {
        const expensesJSON = localStorage.getItem('expenses');
        return expensesJSON ? JSON.parse(expensesJSON) : [];
    }
});
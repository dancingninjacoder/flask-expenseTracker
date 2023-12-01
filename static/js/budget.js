// Function to modify the budget
function modifyBudget() {
    const category = document.getElementById('budgetCategory').value;
    const changeType = document.getElementById('budgetChangeType').value;
    const amount = parseFloat(document.getElementById('budgetAmount').value);
    const goalAmount = parseFloat(document.getElementById('budgetGoalAmount').value);

    // Check if the user has reached their goal
    if (changeType === 'deposit' && budget[category].current + amount > goalAmount) {
        alert("You have reached your goal for this category. Cannot add more funds.");
        return;
    }

    switch (changeType) {
        case 'deposit':
            budget[category].current += amount;
            break;
        case 'deduct':
            if (budget[category].current >= amount) {
                budget[category].current -= amount;
            } else {
                alert("Insufficient funds in the selected budget category.");
                return;
            }
            break;
        default:
            break;
    }

    // Update and save the budget data
    updateBudgetDisplay();
    saveBudgetData();
}

function saveGoalAmount() {
    const category = document.getElementById('budgetCategory').value;
    const goalAmount = parseFloat(document.getElementById('budgetGoalAmount').value);

   

    budget[category].goal = goalAmount;

    // Save the goal amount changes
    saveBudgetData();
    updateBudgetDisplay();
}

// Function to update the budget display
function updateBudgetDisplay() {
    Object.keys(budget).forEach(category => {
        document.getElementById(`${category}Current`).textContent = budget[category].current;
        document.getElementById(`${category}Goal`).textContent = budget[category].goal;
    });
}

// Function to save the budget data to localStorage
function saveBudgetData() {
    localStorage.setItem('budgetData', JSON.stringify(budget));
}

// Function to load the budget data from localStorage
function loadBudgetData() {
    const savedData = localStorage.getItem('budgetData');
    if (savedData) {
        budget = JSON.parse(savedData);
        updateBudgetDisplay();
    }
}

// Initial budget data
let budget = {
    utilities: { current: 0, goal: 0 },
    personal: { current: 0, goal: 0 },
    discretionary: { current: 0, goal: 0 }
};

// Load saved data on page load
loadBudgetData();

function goToHomePage() {
    window.location.href = 'homePage.html';
}

function resetValues() {
    localStorage.clear();
    alert("Local Storage has been cleared.");
}

// Initially display budget
updateBudgetDisplay();
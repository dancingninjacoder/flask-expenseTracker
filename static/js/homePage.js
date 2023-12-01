//let income = 2000;
import { fetchDB, getUserBudgetAmounts } from "../db/practice.js";

// Updates balance and income when the home page is loaded.
const budgetElement = document.getElementById("currentBalance");
budgetElement.addEventListener('load',updateBalance());
const incomeElement = document.getElementById("currentIncome");
incomeElement.addEventListener('load',updateIncome());
const expenseElement = document.getElementById("currentExpenses");
incomeElement.addEventListener('load',updateExpense());

// Update current balance
async function updateBalance() { 
    try{
        if(budgetElement){
            let data = await fetchDB();

            //let user = data.currentUser.user;
            let user = "test@test.com"

            let balance = 0
            let acc = data.accounts.find(account => account.email === user)
            
            acc.incomes.forEach(income => {
                balance+= income.amount;
            })
            acc.expenses.forEach(expense => {
                balance-= expense.amount;
            })

            document.getElementById('currentBalance').textContent = "$"+balance; // this uses local db from the practice.js
        }
    }
    catch (error){
        console.log();
    }
}

// Update current income
async function updateIncome(){
    try{
        if(incomeElement){
            let data = await fetchDB();
            let user = "test@test.com"
            let inc = 0
            let acc = data.accounts.find(account => account.email === user)
            
            acc.incomes.forEach(income => {
                inc+= income.amount;
            })

            document.getElementById("currentIncome").textContent = "$"+inc
            // document.getElementById("currentIncome").textContent = 10 //db.accounts[0].budgets[0].amount; // this is just a test
        }
    }
    catch (error){
        console.log();
    }
}


async function updateExpense(){
    try{
        if(incomeElement){
            let data = await fetchDB();
            let user = "test@test.com"
            let exp = 0
            let acc = data.accounts.find(account => account.email === user)

            acc.expenses.forEach(expense => {
                exp+= expense.amount;
            })

            document.getElementById("currentExpenses").textContent = "$"+exp
            // document.getElementById("currentIncome").textContent = 10 //db.accounts[0].budgets[0].amount; // this is just a test
        }
    }
    catch (error){
        console.log();
    }
}
//updateBalance();
//updateIncome();
# main.py
from flask import Flask, render_template, session, redirect, url_for, request, jsonify
from functools import wraps
from passlib.hash import pbkdf2_sha256
from bson.objectid import ObjectId

import pymongo
currentUser =''
app = Flask(__name__)
app.secret_key = "super secret key"

#Database
#client = pymongo.MongoClient("mongodb+srv://salahbucks:salahbucks@clusternaive.rkiskfb.mongodb.net/?retryWrites=true&w=majority")
client = pymongo.MongoClient('localhost', 27017)
db = client['SalahBucks']

#Function to redirect to homePage
@app.route('/homePage')
def homePage():
    return render_template('homePage.html')

#Function to verify if user is logged in or not. If it is redirect to homePage if not to index
@app.route('/', endpoint='index')
def index():        
    if 'username' in session:
        print('You are logged in as ' + session['username'])
        return redirect(url_for('homePage'))
    return render_template('index.html')

#Function to log out, clears the session made on log in
@app.route('/logout')
def logout():
    # Clear the session data or perform any other logout actions
    session.clear()
    # Redirect to the index page
    return redirect(url_for('index'))

#Function to redirect to signup
@app.route('/redirect_signup', endpoint='redirect_signup')
def redirect_signup():
    print("redirecting")
    # Redirect to another route or URL
    return redirect(url_for('sign_up'))

#Function to retrieve sign up form data and to store data into db
@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if (request.method == 'POST'):
        print("inside post")
        users = db.users
        print(users)
        userArr = {
           'email': request.form['signupEmail'],
            'password': request.form['signupPassword']
        }
        print(userArr)
        userArr['password'] = pbkdf2_sha256.encrypt(userArr['password'])
        session['username'] = userArr['email']
        users.insert_one(userArr)
        print(users)
        return redirect(url_for('index'))
    print("outside")
    return render_template('signUp.html')

#Function to login into an existing db account, if not return to index
@app.route('/login', methods=['POST'])
def login():
    user = db.users.find_one({
      "email": request.form['email']
    })

    if user and pbkdf2_sha256.verify(request.form['password'], user['password']):
        session['username'] = request.form['email']
        return redirect(url_for('index'))
    return "Invalid login credentials"



#TO BE DONE
@app.route('/expense', methods=['GET'])
def expense():
    return render_template('expenseTracker.html')

#Function to insert and store expense from add Expense form
@app.route('/processExpense', methods=['POST'])
def processExpense():

    # Find the user document based on some identifier (e.g., email)
    user_email = session['username'] #Find the user that is logged in to insert and retrieve
    document = db.users.find_one({'email': user_email})

    if (request.method == 'POST' and document):
        print("Found user logged in")
        print("Fetching form data...")

        user_id = document.get('_id')
        expenseName = request.form['expenseName']
        expenseAmount = request.form['expenseAmount']
        expenseCategory = request.form['expenseCategory']

        expense_form_data = [
            {
                "name": expenseName,
                "amount": expenseAmount,
                "category": expenseCategory
            }
        ]

        #If the user object id matches then push the new expense into the database user account
        if (db.users.update_one({'_id': user_id}, {'$push': {'expenses': expense_form_data}})): 
            print("Added expense succesfully to the database")
        else:
            print('Error when adding this object to db, check error logs')
    return render_template('expenseTracker.html')    


@app.route('/income')
def income():
    return render_template('IncomeTracking.html')

#Function to insert and store income from MofifyIncome form
@app.route('/processIncome', methods=['POST'])
def processIncome():
    
    # Find the user document based on some identifier (e.g., email)
    user_email = session['username'] #Find the user that is logged in to insert and retrieve
    document = db.users.find_one({'email': user_email})

    if (request.method == 'POST' and document):
        print("Found user logged in")
        print("Fetching form data...")

        user_id = document.get('_id')
        incomeDate = request.form['incomeDate']
        category = request.form['category']
        amount = request.form['amount']
        
        income_form_data = [
            {
                "date": incomeDate,
                "category": category,
                "amount": amount
            }
        ]

        #If the user object id matches then push the new expense into the database user account
        if (db.users.update_one({'_id': user_id}, {'$push': {'incomes': income_form_data}})): 
            print("Added income succesfully to the database")
        else:
            print('Error when adding this object to db, check error logs')
    return redirect(url_for('income'))

#Function to redirect to budget.html
@app.route('/budget')
def budget():
    return render_template('budget.html')

#Function to insert and store budget from ModifyBudget form
@app.route('/processBudget', methods=['POST'])
def processBudget():
        
    # Find the user document based on some identifier (e.g., email)
    user_email = session['username'] #Find the user that is logged in to insert and retrieve
    document = db.users.find_one({'email': user_email})

    if (request.method == 'POST' and document):
        print("Found user logged in")
        print("Fetching form data...")

        user_id = document.get('_id')
        budgetCategory = request.form['budgetCategory']
        budgetChangeType = request.form['budgetChangeType']
        budgetAmount = request.form['budgetAmount']
        budgetGoalAmount = request.form['budgetGoalAmount']
        
        budget_form_data = [
            {
                "category": budgetCategory,
                "type": budgetChangeType,
                "amount": budgetAmount,
                "goal": budgetGoalAmount
            }
        ]

        #If the user object id matches then push the new expense into the database user account
        if (db.users.update_one({'_id': user_id}, {'$push': {'budgets': budget_form_data}})): 
            print("Added income succesfully to the database")
        else:
            print('Error when adding this object to db, check error logs')
    return redirect(url_for('budget'))


#Function to redirect to user.html and display users info
@app.route('/user')
def user():
        
    # Find the user document based on some identifier (e.g., email)
    user_email = session['username'] #Find the user that is logged in to insert and retrieve
    document = db.users.find_one({'email': user_email})
    # user_id = document.get('_id')

    return render_template('user.html', user_data=document)


#Function to change password
@app.route('/changePassword', methods=['POST'])
def changePassword():
       
    # Find the user document based on some identifier (e.g., email)
    user_email = session['username'] #Find the user that is logged in to insert and retrieve
    document = db.users.find_one({'email': user_email})

    if (request.method == 'POST' and document):
        print("Found user logged in")
        print("Fetching form data...")

        user_id = document.get('_id')
        currentPassword = request.form['currentPassword']
        newPassword = request.form['newPassword']
        confirmPassword = request.form['confirmPassword']

        oldPassword = document['password']
        print(oldPassword)

        #If password match then modify
        if(pbkdf2_sha256.verify(currentPassword, oldPassword) and newPassword == confirmPassword):
            if (db.users.update_one({'_id': user_id}, {'$set': {'password': pbkdf2_sha256.encrypt(confirmPassword)}})): 
                print("Updated password succesfully to the database")

        else:
            print('Error when updating password, check error logs')
    return render_template('user.html')

if __name__ == '__main__':
    app.run(debug=True)

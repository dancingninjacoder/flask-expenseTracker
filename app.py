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


#Function to verify if user is logged in or not. If it is redirect to homePage if not to index
@app.route('/', endpoint='index')
def index():        
    if 'username' in session:
        print('You are logged in as ' + session['username'])
        return redirect(url_for('homePage'))
    return render_template('index.html')


#Function to redirect to homePage
@app.route('/homePage')
def homePage():
    # Find the user document based on some identifier (e.g., email)
    user_email = session['username'] #Find the user that is logged in to insert and retrieve
    document = db.users.find_one({'email': user_email})
    total_expense = 0
    total_income =0
    # print(document)
    if 'expenses' in document:
    # if(db.users.find_one({"expenses": {"$exists": True}})):
      
        for data in document['expenses']:
            for list in data:
                for key, val in list.items():
                    if key == 'amount':
                                total_expense+=val
    if 'incomes' in document:
    # if(db.users.find_one({"incomes": {"$exists": True}})):
        print("incomes exists")
        # expDoc = document['expenses']
        print(type(document['incomes']))
        # print(document['income'])
        for data in document['incomes']:
            for list in data:
                for key, val in list.items():
                    if key == 'amount':
                                total_income+=val
        # return render_template('homePage.html', totalExpense=total_expense, totalIncome=total_income)
    balance = total_income-total_expense
    return render_template('homePage.html', totalExpense=total_expense, totalIncome=total_income, totalBalance=balance)

@app.route('/incomeHomepage')
def incomeHomepage():
    # Find the user document based on some identifier (e.g., email)
    user_email = session['username'] #Find the user that is logged in to insert and retrieve
    document = db.users.find_one({'email': user_email})
    amount = 0
    if(db.users.find_one({"income": {"$exists": True}})):
        # expDoc = document['expenses']
        print(type(document['income']))
        # print(document['income'])
        for data in document['income']:
            for list in data:
                for key, val in list.items():
                    if key == 'amount':
                                total+=val
        return render_template('homePage.html', total_income=amount)
    return render_template('homePage.html', total_income=amount)

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
@app.route('/sign_up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':

        print("inside try")
        users = db.users
        existing_user = users.find_one({'email': request.form['signupEmail']})
        print(existing_user)
        if existing_user is None:        
            user_data = {
                'email': request.form['signupEmail'],
                'password': request.form['signupPassword'],
                'budgets': {
                    'Utilities': {'amount': 0, 'goal': 0},
                    'Personal': {'amount': 0, 'goal': 0},
                    'Discretionary': {'amount': 0, 'goal': 0}
                }
            }
            user_data['password'] = pbkdf2_sha256.encrypt(user_data['password'])
            if(users.insert_one(user_data)):
                print("successfull")
            session['username'] = user_data['email']
            return redirect(url_for('index'))
        else:
            return 'That email already exists!'
        # except Exception as e:
        #     # Log the error for debugging
        #     print("An error occurred: ", e)
        #     return 'An error occurred while trying to create your account.'

    return render_template('signUp.html')
    # if (request.method == 'POST'):
    #     print("inside post")
    #     users = db.users
    #     print(users)
    #     userArr = {
    #        'email': request.form['signupEmail'],
    #         'password': request.form['signupPassword']
    #     }
    #     print(userArr)
    #     userArr['password'] = pbkdf2_sha256.encrypt(userArr['password'])
    #     session['username'] = userArr['email']
    #     users.insert_one(userArr)
    #     print(users)
    #     return redirect(url_for('index'))
    # print("outside")
    # return render_template('signUp.html')

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
@app.route('/expense')
def expense():
    # Find the user document based on some identifier (e.g., email)
    user_email = session['username'] #Find the user that is logged in to insert and retrieve
    document = db.users.find_one({'email': user_email})
    name = ""
    amount = 0
    category = ""
    if 'expenses' in document:        # expDoc = document['expenses']
        # print(type(document['income']))
        # print(document['income'])
        for data in document['expenses']:
            for list in data:
                for key, val in list.items():
                    if key == 'name':
                        name = val
                    if key == 'amount':
                        amount = val
                    if key == 'category':
                        category = val
        return render_template('expenseTracker.html', expenseName=name, expenseAmount = amount, expenseCategory = category)
    return render_template('expenseTracker.html', expenseName=name, expenseAmount = amount, expenseCategory = category)

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
                "amount": int(expenseAmount),
                "category": expenseCategory
            }
        ]

        #If the user object id matches then push the new expense into the database user account
        if (db.users.update_one({'_id': user_id}, {'$push': {'expenses': expense_form_data}})): 
            print("Added expense succesfully to the database")
            # print(document['expenses'])
        else:
            print('Error when adding this object to db, check error logs')
    return render_template('expenseTracker.html')    


@app.route('/income')
def income():
    # Find the user document based on some identifier (e.g., email)
    user_email = session['username'] #Find the user that is logged in to insert and retrieve
    document = db.users.find_one({'email': user_email})
    name = ""
    amount = 0
    category = ""
    date = ""

    if 'incomes' in document:
        # expDoc = document['expenses']
        # print(type(document['income']))
        # print(document['income'])
        for data in document['incomes']:
            for list in data:
                for key, val in list.items():
                    if key == 'date':
                        date = val
                    if key == 'name':
                        name = val
                    if key == 'category':
                        category = val
                    if key == 'amount':
                        amount = val
        return render_template('IncomeTracking.html', incomeDate=date, incomeName = name, incomeCategory = category, incomeAmount = amount)
    return render_template('IncomeTracking.html', incomeDate=date, incomeName = name, incomeCategory = category, incomeAmount = amount)

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
        merchantName = request.form['merchantName']
        category = request.form['category']
        amount = request.form['amount']
        
        income_form_data = [
            {
                "date": incomeDate,
                "name": merchantName,
                "category": category,
                "amount": int(amount)
            }
        ]

        #If the user object id matches then push the new expense into the database user account
        if (db.users.update_one({'_id': user_id}, {'$push': {'incomes': income_form_data}})): 
            print("Added income succesfully to the database")
        else:
            print('Error when adding this object to db, check error logs')
    return redirect(url_for('income'))

#Function to redirect to budget.html
    
@app.route('/budget', methods=['GET', 'POST'])
def budget():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        category = request.form['budgetCategory']
        amount = float(request.form['budgetAmount'])  # Convert to float for monetary values
        goal = float(request.form['budgetGoalAmount'])  # Convert to float for monetary values
        db.users.update_one(
            {'email': session['username'], f'budgets.{category}': {'$exists': True}},
            {'$inc': {f'budgets.{category}.amount': amount},
             '$set': {f'budgets.{category}.goal': goal}}
        )
    
    user = db.users.find_one({'email': session['username']})
    budgets = user['budgets'] if user else {}
    print(budgets)
    return render_template('budget.html', budgets=budgets)
    # Find the user document based on some identifier (e.g., email)
    # user_email = session['username'] #Find the user that is logged in to insert and retrieve
    # document = db.users.find_one({'email': user_email})
    # personalAmount=0
    # discretAmount=0
    # utilitiesAmount=0

    # if(db.users.find_one({"budgets": {"$exists": True}})):
    #     data = document['budgets']
    #     print(data)
    #     for list in data:
    #         for dict  in list:
    #             for category in dict.items():
    #                 #0 is key, 1 is value
    #                 if category[0] == 'Utilities':

    #                     utilitiesAmount = category[1]
    #                 if category[0] == 'Personal':
    #                     personalAmount = category[1]
    #                 if category[0] == 'Discretionary':
    #                     discretAmount = category[1]
                    # if key == 'category' and val == "utilities":
                    #      personalAmount+=
                    # if key == 'category' and val == "personal":
                    # if key == 'category' and val == "discretionary":
                    # if key == 'type':
                    #     type = val
                    # if key == 'amount':
                    #     amount = val
                    # if key == 'goal':
                    #     amount = val
    # return render_template('budget.html', util=utilitiesAmount, dis=discretAmount, pers=personalAmount)

#Function to insert and store budget from ModifyBudget form
# @app.route('/processBudget', methods=['POST'])
# def processBudget():
    
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
                "amount": int(budgetAmount),
                "goal": int(budgetGoalAmount)
            }
        ]

        #If the user object id matches then push the new expense into the database user account
        if (db.users.update_one({'_id': user_id}, {'$set': {'budgets': budget_form_data}})): 
            print("Added budget succesfully to the database")
        else:
            print('Error when adding this object to db, check error logs')
    return render_template('budget.html')
    # return redirect(url_for('budget'))


@app.route('/')
def modifyBudget():
    return render_template('budget.html')


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

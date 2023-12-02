# main.py
from flask import Flask, render_template, session, redirect, url_for, request, jsonify
from functools import wraps
from passlib.hash import pbkdf2_sha256
import pymongo

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
@app.route('/expense')
def expense():
    return render_template('expenseTracker.html')

@app.route('/income')
def income():
    return render_template('IncomeTracking.html')

@app.route('/budget')
def budget():
    return render_template('budget.html')

@app.route('/user')
def user():
    return render_template('user.html')


if __name__ == '__main__':
    app.run(debug=True)

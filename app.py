from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from passlib.hash import pbkdf2_sha256
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "super secret key"

# Database connection
client = MongoClient('localhost', 27017)
db = client['SalahBucks']

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('homePage'))
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'username' in session:
        return redirect(url_for('homePage'))

    if request.method == 'POST':
        try:
            users = db.users
            existing_user = users.find_one({'email': request.form['email']})
            
            if existing_user is None:
                hashed_password = pbkdf2_sha256.encrypt(request.form['password'])
                user_data = {
                    'email': request.form['email'],
                    'password': hashed_password,
                    'budgets': {
                        'Utilities': {'amount': 0, 'goal': 0},
                        'Personal': {'amount': 0, 'goal': 0},
                        'Discretionary': {'amount': 0, 'goal': 0}
                    }
                }
                users.insert_one(user_data)
                session['username'] = request.form['email']
                return redirect(url_for('homePage'))
            else:
                return 'That email already exists!'
        except Exception as e:
            # Log the error for debugging
            print("An error occurred: ", e)
            return 'An error occurred while trying to create your account.'

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

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/homePage')
def homePage():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('homePage.html')

@app.route('/expense')
def expense():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('expenseTracker.html')

@app.route('/income')
def income():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('IncomeTracking.html')

@app.route('/user')
def user():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('user.html')

@app.route('/budget', methods=['GET', 'POST'])
def budget():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        category = request.form['category']
        amount = float(request.form['amount'])  # Convert to float for monetary values
        goal = float(request.form['goal'])  # Convert to float for monetary values

        db.users.update_one(
            {'email': session['username'], f'budgets.{category}': {'$exists': True}},
            {'$inc': {f'budgets.{category}.amount': amount},
             '$set': {f'budgets.{category}.goal': goal}}
        )

    user = db.users.find_one({'email': session['username']})
    budgets = user['budgets'] if user else {}
    return render_template('budget.html', budgets=budgets)

if __name__ == '__main__':
    app.run(debug=True)


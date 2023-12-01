# main.py
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signUp.html')

@app.route('/homePage')
def homePage():
    return render_template('homePage.html')

@app.route('/expense')
def expense():
    return render_template('expenseTracker.html')

@app.route('/income')
def income():
    return render_template('IncomeTracking.html')

@app.route('/budget')
def budget():
    return render_template('budget.html')

if __name__ == '__main__':
    app.run(debug=True)

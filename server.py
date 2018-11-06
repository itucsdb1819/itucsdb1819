import os
from flask import Flask,render_template
from dbinit import initialize

app = Flask(__name__)

#initialize("postgres://nisvjghefalram:d71a1603e278196a848c588d0b30f6197e6e7af60690cb36960f279e286bc709@ec2-54-217-249-103.eu-west-1.compute.amazonaws.com:5432/d4jjtkehcs34es")
initialize(os.getenv("DATABASE_URL"))

@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')

@app.route("/login")
def login_page():
    return render_template('login.html')

@app.route("/system")
def system_page():
    return render_template('system.html')

@app.route("/employee")
def employee_page():
    return render_template('employee.html')

@app.route("/expense")
def expense_page():
    return render_template('expense.html')

@app.route("/product")
def product_page():
    return render_template('product.html')

@app.route("/roles_and_permissions")
def roles_and_permissions_page():
    return render_template('roles_and_permissions.html')

@app.route("/sales_report")
def sales_report_page():
    return render_template('sales_report.html')

if __name__ == "__main__":
    app.run()

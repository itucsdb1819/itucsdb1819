import os
from flask import Flask,render_template
from dbinit import initialize
import forms

app = Flask(__name__)

initialize(os.getenv("DATABASE_URL"))

@app.route("/")
@app.route("/home")
def home_page():
    menuItems = forms.Menu.selectMenuItems()
    for item in menuItems:
        print('{}, {}, {}, {}, {}, {}, {}'.format(item[0], item[1], item[2], item[3], item[4], item[5], item[6]))
    return render_template('home.html', name = item[3], path = item[4], iconPath = item[5])

@app.route("/login")
def login_page():
    return render_template('login.html')

@app.route("/system")
def system_page():
    configValues = forms.System.select()
    return render_template('system.html')

@app.route("/employee")
def employee_page():
    employees = forms.Employee.select("WHERE IsActive = true", "", "")
    for item in employees:
        print('{}, {}, {}, {}'.format(item[0], item[1], item[2], item[3]))
    return render_template('employee.html')

@app.route("/expense")
def expense_page():
    return render_template('expense.html')

@app.route("/product")
def product_page():
    products = forms.Product.select("")
    return render_template('product.html')

@app.route("/roles_and_permissions")
def roles_and_permissions_page():
    return render_template('roles_and_permissions.html')

@app.route("/sales_report")
def sales_report_page():
    return render_template('sales_report.html')

if __name__ == "__main__":
    app.run()

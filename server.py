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
    return render_template('home.html', menuItems = menuItems)

@app.route("/login")
def login_page():
    menuItems = forms.Menu.selectMenuItems()
    return render_template('login.html', menuItems = menuItems)

@app.route("/system")
def system_page():
    menuItems = forms.Menu.selectMenuItems()
    configValues = forms.System.select()
    return render_template('system.html', menuItems = menuItems)

@app.route("/employee")
def employee_page():
    menuItems = forms.Menu.selectMenuItems()
    employees = forms.Employee.select("WHERE IsActive = true")
    return render_template('employee.html', menuItems = menuItems)

@app.route("/expense")
def expense_page():
    menuItems = forms.Menu.selectMenuItems()
    return render_template('expense.html', menuItems = menuItems)

@app.route("/product")
def product_page():
    menuItems = forms.Menu.selectMenuItems()
    products = forms.Product.select("")
    return render_template('product.html', menuItems = menuItems)

@app.route("/roles_and_permissions")
def roles_and_permissions_page():
    menuItems = forms.Menu.selectMenuItems()
    return render_template('roles_and_permissions.html', menuItems = menuItems)

@app.route("/sales_report")
def sales_report_page():
    menuItems = forms.Menu.selectMenuItems()
    return render_template('sales_report.html', menuItems = menuItems)

if __name__ == "__main__":
    app.run()

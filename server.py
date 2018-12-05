import os
from flask import Flask,render_template
from dbinit import initialize
import forms

app = Flask(__name__)

initialize(os.getenv("DATABASE_URL"))

menuItems = forms.Menu.selectMenuItems()

def load_resource(resourceId, resourceSet):
    localeId = forms.System.selectSystemValue('SystemLanguage')
    print(localeId)
    print(localeId[0])
    resourceValue = forms.Localization.selectLocalizationItem(resourceId, resourceSet, 'tr')
    print(resourceValue)
    print(resourceValue[0])
    return resourceValue

@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html', menuItems = menuItems)

@app.route("/login")
def login_page():
    return render_template('login.html', menuItems = menuItems)

@app.route("/system")
def system_page():
    configValues = forms.System.select()
    return render_template('system.html', menuItems = menuItems)

@app.route("/employee")
@app.route("/employee/index")
def employee_page():
    return render_template('employee.html', menuItems = menuItems, load_resource = load_resource)

@app.route("/employee_create")
def employee_create_page():
    return render_template('employee_create.html', menuItems = menuItems)

@app.route("/expense")
def expense_page():
    return render_template('expense.html', menuItems = menuItems)

@app.route("/product")
def product_page():
    products = forms.Product.select("")
    return render_template('product.html', menuItems = menuItems)

@app.route("/roles_and_permissions")
def roles_and_permissions_page():
    return render_template('roles_and_permissions.html', menuItems = menuItems)

@app.route("/sales")
@app.route("/sales/report")
def sales_report_page():
    return render_template('sales_report.html', menuItems = menuItems)

@app.route("/sales/create")
def sales_create():
    return render_template('sales_create.html', menuItems = menuItems)

if __name__ == "__main__":
    app.run()

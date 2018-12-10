import os
from flask import Flask,render_template,redirect,url_for, request
from dbinit import initialize
import forms

app = Flask(__name__)

initialize(os.getenv("DATABASE_URL"))

menuItems = forms.Menu.selectMenuItems()

def load_resource(resourceId, resourceSet):
    localeId = forms.System.selectSystemValue('SystemLanguage')
    resourceValue = forms.Localization.selectLocalizationItem(resourceId, resourceSet, localeId[0])
    return resourceValue[0]

def isLoggedIn():
    print(forms.userId)
    if forms.userId == None:
        return False

@app.route("/")
@app.route("/home", endpoint = "home")
def home_page():
    if isLoggedIn():
        return render_template('home.html', menuItems = menuItems)
    return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'], endpoint = "login")
def login_page():
    error = None
    if request.method == 'POST':
        if forms.Employee.login(request.form['username'], request.form['password']) == True:
            return redirect(url_for('home'))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error = error, load_resource = load_resource)

@app.route("/system")
def system_page():
    configValues = forms.System.select()
    return render_template('system.html', menuItems = menuItems)

@app.route("/employee")
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

@app.route("/roles_and_permissions", methods=['GET', 'POST'], endpoint="roles_and_permissions")
def roles_and_permissions_page():
    roles = forms.Role.select()
    selectedRoleId = 0
    if request.method == 'POST':
        selectedRoleId = request.form.get('selectedRole')
    
    selectedRole = forms.Role.selectWithID(selectedRoleId)
    rolesAndPermissions = forms.RolePermission.selectRolePermissions(selectedRoleId)

    return render_template('roles_and_permissions.html', menuItems = menuItems, load_resource = load_resource, selectedRole = selectedRole, roles = roles)

@app.route("/roles_and_permissions_update", methods=['POST'])
def roles_and_permissions_insert():
    permissions = request.form.getlist('permission')

    redirect(url_for('roles_and_permissions'))

@app.route("/sales")
def sales_report_page():
    return render_template('sales_report.html', menuItems = menuItems)

@app.route("/sales_create")
def sales_create():
    return render_template('sales_create.html', menuItems = menuItems)

if __name__ == "__main__":
    app.run()

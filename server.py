import os
from flask import Flask,render_template,redirect,url_for, request, session, escape
from dbinit import initialize
import forms

app = Flask(__name__)

app.secret_key = b'secretkeyissecret'

initialize(os.getenv("DATABASE_URL"))

menuItems = forms.Menu.selectMenuItems()

def load_resource(resourceId, resourceSet):
    localeId = forms.System.selectSystemValue('SystemLanguage')
    if resourceId == None:
        resourceId = ''
    resourceValue = forms.Localization.selectLocalizationItem(resourceId, resourceSet, localeId[0])
    return resourceValue[0]

@app.route("/")
@app.route("/home", endpoint = "home")
def home_page():
    if 'userId' in session:
        return render_template('home.html', menuItems = menuItems)
    return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'], endpoint = "login")
def login_page():
    error = None
    if request.method == 'POST':
        if forms.Employee.login(request.form['username'], request.form['password']) == True:
            session['userId'] = request.form['username']
            return redirect(url_for('home'))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error = error, load_resource = load_resource)

@app.route('/logout')
def logout():
    session.pop('userId', None)
    return redirect(url_for('home'))


@app.route("/system")
def system_page():
    if 'userId' in session:
        configValues = forms.System.select()
        return render_template('system.html', menuItems = menuItems)
    return redirect(url_for('login'))

@app.route("/employee")
def employee_page():
    if 'userId' in session:
        return render_template('employee.html', menuItems = menuItems, load_resource = load_resource)
    return redirect(url_for('login'))

@app.route("/employee_create")
def employee_create_page():
    if 'userId' in session:
        return render_template('employee_create.html', menuItems = menuItems)
    return redirect(url_for('login'))

@app.route("/expense")
def expense_page():
    if 'userId' in session:
        return render_template('expense.html', menuItems = menuItems)
    return redirect(url_for('login'))

@app.route("/product")
def product_page():
    if 'userId' in session:
        products = forms.Product.select("")
        return render_template('product.html', menuItems = menuItems)
    return redirect(url_for('login'))

@app.route("/roles_and_permissions", methods=['GET', 'POST'], endpoint="roles_and_permissions")
def roles_and_permissions_page():
    if 'userId' in session:
        roles = forms.Role.select()
        selectedRoleId = 0
        if request.method == 'POST':
            if request.form['submit_button'] == 'insertPermission':
                permissions = request.form.getlist('permission')
                print("You are here")
                for permission in permissions:
                    print(permission)
                return redirect(url_for('roles_and_permissions'))
            elif request.form['submit_button'] == 'selectRole':
                selectedRoleId = request.form.get('selectedRole')
        selectedRole = forms.Role.selectWithID(selectedRoleId)
        rolesAndPermissions = forms.RolePermission.selectRolePermissions(selectedRoleId)
        return render_template('roles_and_permissions.html', menuItems = menuItems, load_resource = load_resource, selectedRole = selectedRole, rolesAndPermissions = rolesAndPermissions, roles = roles)
    else:
        return redirect(url_for('login'))


@app.route("/sales")
def sales_report_page():
    if 'userId' in session:
        return render_template('sales_report.html', menuItems = menuItems)
    return redirect(url_for('login'))

@app.route("/sales_create")
def sales_create():
    if 'userId' in session:
        return render_template('sales_create.html', menuItems = menuItems)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run()

import os
from flask import Flask,render_template,redirect,url_for, request, session, escape
from dbinit import initialize
import forms
import traceback

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
    try:
        if ('userId' in session):
            if forms.Permission.hasPermission(session['roleId'], 'HomePage.Access'):
                return render_template('home.html', menuItems = menuItems)
            else:
                return redirect(url_for('unauthorized'))
        return redirect(url_for('login', error = load_resource('Error.SessionExpired', 'PageText')))
    except Exception as error:
        forms.System.insertLog(error, 'home', 'Fatal', traceback.format_exc())
        return redirect(url_for('error', errorMessage = error))

@app.route("/error", endpoint = "error")
def error_page():
    errorMessage = request.args.get('errorMessage')
    return render_template('error.html', load_resource = load_resource, errorMessage = errorMessage, menuItems = menuItems)

@app.route("/unauthorized", endpoint = "unauthorized")
def unauthorized_page():
    try:
        user = 'userId' in session
        forms.System.insertLog('Unauthorized access was made by user: {}'.format(user) , 'unauthorized', 'Warning', '')
        return render_template('unauthorized.html', load_resource = load_resource, menuItems = menuItems)
    except Exception as error:
        forms.System.insertLog(error, 'unauthorized', 'Fatal', traceback.format_exc())
        return redirect(url_for('error', errorMessage = error))

@app.route("/login", methods=['GET', 'POST'], endpoint = "login")
def login_page():
    try:
        error = request.args.get('error')
        if request.method == 'POST':
            if forms.Employee.login(request.form['username'], request.form['password']) == True:
                employee = forms.Employee.selectEmployee(request.form['username'], request.form['password'])
                forms.System.insertLog('User {} logged in.'.format(request.form['username']), 'login', 'Info', '')
                session['userId'] = employee[0]
                session['roleId'] = employee[3]
                return redirect(url_for('home'))
            else:
                forms.System.insertLog('User {} attempted unsuccessful login.'.format(request.form['username']), 'login', 'Warning', '')
                error = load_resource('Error.InvalidCredentials', 'PageText')
        return render_template('login.html', error = error, load_resource = load_resource)
    except Exception as error:
        forms.System.insertLog(error, 'login', 'Fatal', traceback.format_exc())
        return redirect(url_for('error', errorMessage = error))

@app.route('/logout')
def logout():
    try:
        oldUser = 'userId' in session
        session.pop('userId', None)
        forms.System.insertLog('User {} logged in.'.format(oldUser), 'login', 'Info', '')
        return redirect(url_for('login'))
    except Exception as error:
        forms.System.insertLog(error, 'logout', 'Fatal', traceback.format_exc())
        return redirect(url_for('error', errorMessage = error))

@app.route("/system")
def system_page():
    try:
        if 'userId' in session:
            if forms.Permission.hasPermission(session['roleId'], 'SystemPage.Access'):
                configValues = forms.System.select()
                logs = forms.System.getSystemLogs()
                return render_template('system.html', menuItems = menuItems, load_resource = load_resource, configValues = configValues, logs = logs)
            else:
                return redirect(url_for('unauthorized'))
        return redirect(url_for('login', error = load_resource('Error.SessionExpired', 'PageText')))
    except Exception as error:
        forms.System.insertLog(error, 'system', 'Fatal', traceback.format_exc())
        return redirect(url_for('error', errorMessage = error))

@app.route("/employee")
def employee_page():
    try:
        if 'userId' in session:
            if forms.Permission.hasPermission(session['roleId'], 'EmployeePage.Access'):
                return render_template('employee.html', menuItems = menuItems, load_resource = load_resource)
            else:
                return redirect(url_for('unauthorized'))
        return redirect(url_for('login', error = load_resource('Error.SessionExpired', 'PageText')))
    except Exception as error:
        forms.System.insertLog(error, 'employee', 'Fatal', traceback.format_exc())
        return redirect(url_for('error', errorMessage = error))

@app.route("/employee_create")
def employee_create_page():
    try:
        if 'userId' in session:
            if forms.Permission.hasPermission(session['roleId'], 'EmployeePage.Access'):
                return render_template('employee_create.html', menuItems = menuItems, load_resource = load_resource)
            else:
                return redirect(url_for('unauthorized'))
        return redirect(url_for('login', error = load_resource('Error.SessionExpired', 'PageText')))
    except Exception as error:
        forms.System.insertLog(error, 'employee_create', 'Fatal', traceback.format_exc())
        return redirect(url_for('error', errorMessage = error))

@app.route("/expense")
def expense_page():
    try:
        if 'userId' in session:
            if forms.Permission.hasPermission(session['roleId'], 'ExpensePage.Access'):
                return render_template('expense.html', menuItems = menuItems, load_resource = load_resource)
            else:
                return redirect(url_for('unauthorized'))
        return redirect(url_for('login', error = load_resource('Error.SessionExpired', 'PageText')))
    except Exception as error:
        forms.System.insertLog(error, 'expense', 'Fatal', traceback.format_exc())
        return redirect(url_for('error', errorMessage = error))

@app.route("/product")
def product_page():
    try:
        if 'userId' in session:
            if forms.Permission.hasPermission(session['roleId'], 'ProductPage.Access'):
                products = forms.Product.select("")
                return render_template('product.html', menuItems = menuItems)
            else:
                return redirect(url_for('unauthorized'))
        return redirect(url_for('login', error = load_resource('Error.SessionExpired', 'PageText')))
    except Exception as error:
        forms.System.insertLog(error, 'product', 'Fatal', traceback.format_exc())
        return redirect(url_for('error', errorMessage = error))

@app.route("/roles_and_permissions", methods=['GET', 'POST'], endpoint="roles_and_permissions")
def roles_and_permissions_page():
    try:
        if 'userId' in session:
            if forms.Permission.hasPermission(session['roleId'], 'RolesAndPermissionsPage.Access'):
                roles = forms.Role.select()
                selectedRoleId = 0
                if request.method == 'POST':
                    if request.form['submit_button'] == 'insertPermission':
                        permissions = request.form.getlist('permission')
                        role = request.form.get('selectedRoleID')
                        roleName = request.form.get('selectedRoleName')
                        forms.RolePermission.insertPermissions(role, roleName, permissions)                
                        return redirect(url_for('roles_and_permissions'))
                    elif request.form['submit_button'] == 'selectRole':
                        selectedRoleId = request.form.get('selectedRole')
                selectedRole = forms.Role.selectWithID(selectedRoleId)
                rolesAndPermissions = forms.RolePermission.selectRolePermissions(selectedRoleId)
                return render_template('roles_and_permissions.html', menuItems = menuItems, load_resource = load_resource, selectedRole = selectedRole, rolesAndPermissions = rolesAndPermissions, roles = roles)
            else:
                return redirect(url_for('unauthorized'))
        else:
            return redirect(url_for('login', error = load_resource('Error.SessionExpired', 'PageText')))
    except Exception as error:
        forms.System.insertLog(error, 'roles_and_permissions', 'Fatal', traceback.format_exc())
        return redirect(url_for('error', errorMessage = error))


@app.route("/sales", methods=['GET', 'POST'])
def sales_report_page():
    try:
        if 'userId' in session:
            if forms.Permission.hasPermission(session['roleId'], 'SalesPage.Access'):
                selectedEmployee = 0
                selectedRegister = 0
                if request.method == 'POST':
                    selectedEmployee = request.form.get('selectedEmployee')
                    selectedRegister = request.form.get('selectedRegister')
                report = forms.Sale.getReport(selectedRegister, selectedEmployee)
                employees = forms.Employee.select()
                registers = forms.Registers.select()
                return render_template('sales_report.html', report = report, menuItems = menuItems, load_resource = load_resource, employees = employees, registers = registers)
            else:
                return redirect(url_for('unauthorized'))
        return redirect(url_for('login', error = load_resource('Error.SessionExpired', 'PageText')))
    except Exception as error:
        forms.System.insertLog(error, 'sales', 'Fatal', traceback.format_exc())
        return redirect(url_for('error', errorMessage = error))

@app.route("/sales_create")
def sales_create():
    try:
        if 'userId' in session:
            if forms.Permission.hasPermission(session['roleId'], 'SalesPage.Access'):
                return render_template('sales_create.html', menuItems = menuItems)
            else:
                return redirect(url_for('unauthorized'))
        return redirect(url_for('login', error = load_resource('Error.SessionExpired', 'PageText')))
    except Exception as error:
        forms.System.insertLog(error, 'sales_create', 'Fatal', traceback.format_exc())
        return redirect(url_for('error', errorMessage = error))

if __name__ == "__main__":
    app.run()

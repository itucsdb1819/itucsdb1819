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
        forms.System.insertLog(str(error), 'home', 'Fatal', traceback.format_exc())
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
        forms.System.insertLog(str(error), 'unauthorized', 'Fatal', traceback.format_exc())
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
        forms.System.insertLog(str(error), 'login', 'Fatal', traceback.format_exc())
        return redirect(url_for('error', errorMessage = error))

@app.route('/logout')
def logout():
    try:
        oldUser = 'userId' in session
        session.pop('userId', None)
        forms.System.insertLog('User {} logged in.'.format(oldUser), 'login', 'Info', '')
        return redirect(url_for('login'))
    except Exception as error:
        forms.System.insertLog(str(error), 'logout', 'Fatal', traceback.format_exc())
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
        forms.System.insertLog(str(error), 'system', 'Fatal', traceback.format_exc())
        return redirect(url_for('error', errorMessage = error))

@app.route("/employee", methods = ['GET', 'POST'], endpoint = "employee")
def employee_page():
    try:
        if 'userId' in session:
            if forms.Permission.hasPermission(session['roleId'], 'EmployeePage.Access'):
                employees = forms.Employee.select()
                return render_template('employee.html', menuItems = menuItems, load_resource = load_resource, employees = employees)
            else:
                return redirect(url_for('unauthorized'))
        return redirect(url_for('login', error = load_resource('Error.SessionExpired', 'PageText')))
    except Exception as error:
        forms.System.insertLog(str(error), 'employee', 'Fatal', traceback.format_exc())
        return redirect(url_for('error', errorMessage = error))

@app.route("/employee_delete", methods=['GET', 'POST'])
def employee_delete():
    try:
        employeeID = request.args.get('id')
        forms.Employee.deleteEmployee(employeeID)
        return redirect(url_for("employee"))
    except Exception as error:
        forms.System.insertLog(str(error), 'employee_delete', 'Fatal', traceback.format_exc())
        return redirect(url_for('error', errorMessage = error))

@app.route("/employee_create", methods = ['GET', 'POST'], endpoint = "employee_create")
def employee_create_page():
    try:
        if 'userId' in session:
            if forms.Permission.hasPermission(session['roleId'], 'EmployeePage.Access'):             
                
                if request.method == 'POST':
                    employeeID = request.form.get('employeeID')
                    print(employeeID)
                    role = request.form.get('Role')
                    title = request.form.get('Title')
                    name = request.form.get('Name')
                    surname = request.form.get('Surname')
                    username = request.form.get('Username')
                    if employeeID != None:
                        forms.Employee.updateEmployee(employeeID, role, title, name, surname, username)
                    else:
                        forms.Employee.saveEmployee(role, title, name, surname, username)
                    return redirect(url_for("employee"))

                employeeID = request.args.get('id')
                roleID = 0
                titleID = 0
                name = ""
                surname = ""
                username = ""
                
                if employeeID != None:
                    employee = forms.Employee.selectEmployeeByID(employeeID)
                    name = employee[2]
                    surname = employee[3]
                    username = employee[8]
                    roleID = employee[1]
                    titleID = employee[7]

                roles = forms.Role.select()
                titles = forms.Title.select()
                return render_template('employee_create.html', employeeID = employeeID, menuItems = menuItems, load_resource = load_resource, roles = roles, titles = titles, roleID = roleID, titleID = titleID, name = name, surname = surname, username = username)
            else:
                return redirect(url_for('unauthorized'))
        return redirect(url_for('login', error = load_resource('Error.SessionExpired', 'PageText')))
    except Exception as error:
        forms.System.insertLog(str(error), 'employee_create', 'Fatal', traceback.format_exc())
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
        forms.System.insertLog(str(error), 'expense', 'Fatal', traceback.format_exc())
        return redirect(url_for('error', errorMessage = error))

@app.route("/product_delete", methods=['GET', 'POST'])
def product_delete():
    try:
        productID = request.args.get('id')
        forms.Product.deleteProduct(productID)
        return redirect(url_for("product"))
    except Exception as error:
        forms.System.insertLog(str(error), 'product_delete', 'Fatal', traceback.format_exc())
        return redirect(url_for('error', errorMessage = error))

@app.route("/product", endpoint = "product")
def product_page():
    try:
        if 'userId' in session:
            if forms.Permission.hasPermission(session['roleId'], 'ProductPage.Access'):
                products = forms.Product.select()
                toys = forms.Product.selectToys()
                return render_template('product.html', menuItems = menuItems, load_resource = load_resource, products = products)
            else:
                return redirect(url_for('unauthorized'))
        return redirect(url_for('login', error = load_resource('Error.SessionExpired', 'PageText')))
    except Exception as error:
        forms.System.insertLog(str(error), 'product', 'Fatal', traceback.format_exc())
        return redirect(url_for('error', errorMessage = error))

@app.route("/product_create", methods = ['GET', 'POST'], endpoint="product_create")
def product_create_page():
    try:
        if 'userId' in session:
            if forms.Permission.hasPermission(session['roleId'], 'ProductPage.Access'):
                if request.method == 'POST':
                    productID = request.form.get('productID')
                    productType = request.form.get('ProductType')
                    name = request.form.get('Name')
                    price = request.form.get('Price')
                    calorie = request.form.get('Calorie')
                    carbonhydrate = request.form.get('Carbonhydrate')
                    fat = request.form.get('Fat')
                    glucose = request.form.get('Glucose')
                    isVegetarian = request.form.get('IsVegetarian')
                    if productID != None:
                        forms.Product.updateProduct(productID, productType, name, price, calorie, carbonhydrate, fat, glucose, isVegetarian)
                    else:
                        forms.Product.createProduct(productType, name, price, calorie, carbonhydrate, fat, glucose, isVegetarian)                        
                    return redirect(url_for("product_create"))

                productID = request.args.get('id')
                price = 0
                calorie = 0
                carbonhydrate = 0
                fat = 0
                calorie = 0
                glucose = 0
                isVegetarian = False
                name = ""
                
                if productID != None:
                    product = forms.Product.selectWithID(productID)
                    productTypeID = product[1]
                    name = product[2]
                    price = product[3]
                    calorie = product[4]
                    carbonhydrate = product[5]
                    fat = product[6]
                    calorie = product[7]
                    glucose = product[8]
                    isVegetarian = product[9]

                productTypes = forms.Product.selectProductTypes()
                return render_template('product_create.html', menuItems = menuItems, load_resource = load_resource, productTypes = productTypes, productType = productType, productID = productID, name = name, price = price, calorie = calorie, carbonhydrate = carbonhydrate, fat = fat, glucose = glucose, isVegetarian = isVegetarian)
            else:
                return redirect(url_for('unauthorized'))
        return redirect(url_for('login', error = load_resource('Error.SessionExpired', 'PageText')))
    except Exception as error:
        forms.System.insertLog(str(error), 'product', 'Fatal', traceback.format_exc())
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
        forms.System.insertLog(str(error), 'roles_and_permissions', 'Fatal', traceback.format_exc())
        return redirect(url_for('error', errorMessage = error))


@app.route("/sales", methods=['GET', 'POST'], endpoint="sales")
def sales_report_page():
    try:
        if 'userId' in session:
            if forms.Permission.hasPermission(session['roleId'], 'SalesPage.Access'):
                selectedEmployee = 0
                selectedRegister = 0
                report = forms.Sale.getWholeReport()
                if request.method == 'POST':
                    selectedEmployee = request.form.get('selectedEmployee')
                    selectedRegister = request.form.get('selectedRegister')
                    report = forms.Sale.getReport(selectedRegister, selectedEmployee)
                employees = forms.Employee.select()
                registers = forms.Register.select()
                return render_template('sales_report.html', report = report, menuItems = menuItems, load_resource = load_resource, employees = employees, registers = registers)
            else:
                return redirect(url_for('unauthorized'))
        return redirect(url_for('login', error = load_resource('Error.SessionExpired', 'PageText')))
    except Exception as error:
        forms.System.insertLog(str(error), 'sales', 'Fatal', traceback.format_exc())
        return redirect(url_for('error', errorMessage = error))

@app.route("/sales_create", methods=['GET', 'POST'])
def sales_create():
    try:
        if 'userId' in session:
            if forms.Permission.hasPermission(session['roleId'], 'SalesPage.Access'):
                if request.method == 'POST':
                    selectedEmployee = request.form.get('Employee')
                    selectedRegister = request.form.get('Register')
                    product = request.form.get('Product')
                    print(product)
                    paymentMethod = request.form.get('PaymentMethod')
                    isDelivered = request.form.get('IsDelivered')
                    isCancelled = request.form.get('IsCancelled')
                    forms.Sale.insert(selectedEmployee, selectedRegister, paymentMethod, isDelivered, isCancelled, product)
                employees = forms.Employee.select()
                registers = forms.Register.select()
                products = forms.Product.select()
                return render_template('sales_create.html', menuItems = menuItems, load_resource = load_resource, employees = employees, registers = registers, products = products)
            else:
                return redirect(url_for('unauthorized'))
        return redirect(url_for('login', error = load_resource('Error.SessionExpired', 'PageText')))
    except Exception as error:
        stackTrace = traceback.format_exc()
        print(stackTrace)
        forms.System.insertLog(str(error), 'sales_create', 'Fatal', stackTrace)
        return redirect(url_for('error', errorMessage = error))

if __name__ == "__main__":
    app.run()

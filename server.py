from flask import Flask,render_template
from dbinit import initialize

app = Flask(__name__)

initialize("dbname='postgres' user='postgres' host='localhost' password='hastayimpw'")


@app.route("/")
@app.route("/home")
def home_page():
    render_template('home.html')

@app.route("/login")
def login_page():
    render_template('login.html')

@app.route("/system")
def system_page():
    render_template('system.html')

@app.route("/employee")
def system_page():
    render_template('employee.html')

@app.route("/expense")
def home_page():
    render_template('expense.html')

@app.route("/product")
def login_page():
    render_template('product.html')

@app.route("/roles_and_permissions")
def system_page():
    render_template('roles_and_permissions.html')

@app.route("/sales_report")
def system_page():
    render_template('sales_report.html')

if __name__ == "__main__":
    app.run()

import psycopg2 as dbapi
import datetime

url = "dbname='postgres' user='postgres' host='localhost' password='hastayimpw'"

class Employee:
    def __init__(id, name, surname, roleId, titleId):
        self.employeeId = id
        self.name = name
        self.surname = surname
        self.roleId = roleId
        self.titleId = titleId

    def save(employee):
        with dbapi.connect(url) as conn
            cursor = connection.cursor()
            cursor.execute('INSERT INTO Employee (RoleID, Name, Surname, CreatedOn, ModifiedOn, IsActive, TitleID) VALUES (%d, %s, %s, %s, %s, %s, %s)' % (employee.roleId, employee.name, employee.surname, employee.createdOn, None, True, datetime.now))
            connection.commit()
            cursor.close()

    def delete(employeeId):
        with dbapi.connect(url) as conn
            cursor = connection.cursor()
            cursor.execute('UPDATE Employee SET IsActive = false WHERE EmployeeID = ' + employeeId)
            connection.commit()
            cursor.close()

class System:
    def __init__(id, configValue, configValueType, isEditable):
        self.configId = id
        self.configValue = configValue
        self.configValueType = configValueType
        self.isEditable = isEditable
    
    def update(configId, configValue, employeeId):
        with dbapi.connect(url) as conn
            cursor = connection.cursor()
            cursor.execute('UPDATE Config SET ConfigValue = %s, ModifiedBy = %s, ModifiedOn = %s WHERE ConfigId = %s AND IsEditable = true' % (configValue, employeeId, datetime.now, configId))
            connection.commit()
            cursor.close()

import psycopg2 as dbapi
import datetime
import os

url = os.getenv("DATABASE_URL")

class Employee:
    def __init__(id, name, surname, roleId, titleId):
        self.employeeId = id
        self.name = name
        self.surname = surname
        self.roleId = roleId
        self.titleId = titleId

    def save(employee):
        conn = dbapi.connect(url)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Employee (RoleID, Name, Surname, CreatedOn, ModifiedOn, IsActive, TitleID) VALUES (%d, %s, %s, %s, %s, %s, %s)' % (employee.roleId, employee.name, employee.surname, employee.createdOn, None, True, datetime.now))
        conn.commit()
        cursor.close()
        conn.close()

    def delete(employeeId):
        conn = dbapi.connect(url)
        cursor = conn.cursor()
        cursor.execute('UPDATE Employee SET IsActive = false WHERE EmployeeID = ' + employeeId)
        conn.commit()
        cursor.close()
        conn.close()

class System:
    def __init__(id, configValue, configValueType, isEditable):
        self.configId = id
        self.configValue = configValue
        self.configValueType = configValueType
        self.isEditable = isEditable
    
    def update(configId, configValue, employeeId):
        conn = dbapi.connect(url)
        cursor = conn.cursor()
        cursor.execute('UPDATE Config SET ConfigValue = %s, ModifiedBy = %s, ModifiedOn = %s WHERE ConfigId = %s AND IsEditable = true' % (configValue, employeeId, datetime.now, configId))
        conn.commit()
        cursor.close()
        conn.close()

class Menu:
    def __init__(menuItemId, masterMenuItemId, permissionId, menuItemName, menuItemPath, iconPath, isActive):
        self.menuItemId = menuItemId
        self.masterMenuItemId = masterMenuItemId
        self.permissionId = permissionId
        self.menuItemName = menuItemName
        self.menuItemPath = menuItemPath
        self.iconPath = iconPath
        self.isActive = isActive

    def select():
        conn = dbapi.connect(url)
        cursor = conn.cursor()
        queryString = """SELECT * FROM Menu WHERE IsActive = 1"""
        retVal = cursor.execute(queryString)
        conn.commit()
        cursor.close()
        conn.close()        
        return retVal

    selectStatement = "SELECT * FROM Menu WHERE IsActive = 1"
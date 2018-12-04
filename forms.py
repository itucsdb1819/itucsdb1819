import psycopg2 as dbapi
import datetime
import os

url = os.getenv("DATABASE_URL")

def selectMenuItems():
    conn = dbapi.connect(url)
    cursor = conn.cursor()
    queryString = """SELECT MenuItemID, MasterMenuItemID, PermissionID, MenuItemName, MenuItemPath, IconPath, IsActive FROM Menu WHERE IsActive = 1"""
    cursor.execute(queryString)
    for row in cursor:
        menuItemId, masterMenuItemId, permissionId, menuItemName, menuItemPath, iconPath, isActive = row
        print('{}, {}, {}, {}, {}, {}, {}'.format(menuItemId, masterMenuItemId, permissionId, menuItemName, menuItemPath, iconPath, isActive))
    menuItems = cursor.fetchall()
    return menuItems

def saveEmployee(employee):
    conn = dbapi.connect(url)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Employee (RoleID, Name, Surname, CreatedOn, ModifiedOn, IsActive, TitleID) VALUES (%d, %s, %s, %s, %s, %s, %s)' % (employee.roleId, employee.name, employee.surname, employee.createdOn, None, True, datetime.now))
    conn.commit()
    cursor.close()
    conn.close()

def deleteEmployee(employeeId):
    conn = dbapi.connect(url)
    cursor = conn.cursor()
    cursor.execute('UPDATE Employee SET IsActive = false WHERE EmployeeID = ' + employeeId)
    conn.commit()
    cursor.close()
    conn.close()

def updateSystemEntry(configId, configValue, employeeId):
    conn = dbapi.connect(url)
    cursor = conn.cursor()
    cursor.execute('UPDATE Config SET ConfigValue = %s, ModifiedBy = %s, ModifiedOn = %s WHERE ConfigId = %s AND IsEditable = true' % (configValue, employeeId, datetime.now, configId))
    conn.commit()
    cursor.close()
    conn.close()

class Employee:
    def __init__(id, name, surname, roleId, titleId):
        self.employeeId = id
        self.name = name
        self.surname = surname
        self.roleId = roleId
        self.titleId = titleId    

class System:
    def __init__(id, configValue, configValueType, isEditable):
        self.configId = id
        self.configValue = configValue
        self.configValueType = configValueType
        self.isEditable = isEditable  
    
class Menu:
    def __init__(menuItemId, masterMenuItemId, permissionId, menuItemName, menuItemPath, iconPath, isActive):
        self.menuItemId = menuItemId
        self.masterMenuItemId = masterMenuItemId
        self.permissionId = permissionId
        self.menuItemName = menuItemName
        self.menuItemPath = menuItemPath
        self.iconPath = iconPath
        self.isActive = isActive

    

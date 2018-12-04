import psycopg2 as dbapi
import datetime
import os

url = os.getenv("DATABASE_URL")

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

    def saveEmployee(employee):
        conn = dbapi.connect(url)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Employee (RoleID, Name, Surname, CreatedOn, ModifiedOn, IsActive, TitleID) VALUES (%d, %s, %s, %s, %s, %s, %s)' % (employee.roleId, employee.name, employee.surname, employee.createdOn, None, True, datetime.now))
        conn.commit()
        cursor.close()
        conn.close()

    def select(whereClause, orderByClause, groupByClause):
        conn = dbapi.connect(url)
        cursor = conn.cursor()
        queryString = """SELECT EmployeeID, RoleID, Name, Surname, 
        CreatedOn, ModifiedOn, IsActive, TitleID, Username FROM Employee """ + whereClause + orderByClause + groupByClause
        employees = cursor.fetchAll()
        cursor.close()
        return employees


class System:
    def __init__(configId, configValue, configValueType, isEditable):
        self.configId = configId
        self.configValue = configValue
        self.configValueType = configValueType
        self.isEditable = isEditable  

    def select():
        conn = dbapi.connect(url)
        cursor = conn.cursor()
        queryString = """SELECT ConfigID, ConfigValue, ConfigValueType, IsEditable FROM System"""
        cursor.execute(queryString)
        systemItems = cursor.fetchall()
        cursor.close()
        return systemItems
    
class Menu:
    def __init__(menuItemId, masterMenuItemId, permissionId, menuItemName, menuItemPath, iconPath, isActive):
        self.menuItemId = menuItemId
        self.masterMenuItemId = masterMenuItemId
        self.permissionId = permissionId
        self.menuItemName = menuItemName
        self.menuItemPath = menuItemPath
        self.iconPath = iconPath
        self.isActive = isActive

    def selectMenuItems():
        conn = dbapi.connect(url)
        cursor = conn.cursor()
        queryString = """SELECT MenuItemID, MasterMenuItemID, PermissionID, MenuItemName, MenuItemPath, IconPath, IsActive FROM Menu WHERE IsActive = true"""
        cursor.execute(queryString)
        menuItems = cursor.fetchall()
        cursor.close()
        return menuItems

class Permission:
    def __init__(permissionID, permissionCode, permissionName):
        self.permissionID = permissionID
        self.permissionCode = permissionCode
        self.permissionName = permissionName    

class Product:
    def __init__(productID, productTypeID, productName, price, calorie, protein, carbonhydrate, fat, glucose, isVegetarian):
        self.productID = productID
        self.productTypeID = productTypeID
        self.productName = productName
        self.price = price
        self.calorie = calorie
        self.protein = protein
        self.carbonhydrate = carbonhydrate
        self.fat = fat
        self.glucose = glucose
        self.isVegetarian = isVegetarian

class Localization:
    def __init__(pk, resourceID, localeID, resourceSet, value):
        self.pk = pk
        self.resourceID = resourceID
        self.localeID = localeID
        self.resourceSet = resourceSet
        self.value = value
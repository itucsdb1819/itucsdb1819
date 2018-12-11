import psycopg2 as dbapi
import datetime
import os

url = os.getenv("DATABASE_URL")

userId = None

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

    def select(clause):
        conn = dbapi.connect(url)
        cursor = conn.cursor()
        queryString = """SELECT EmployeeID, RoleID, Name, Surname, 
        CreatedOn, ModifiedOn, IsActive, TitleID, Username FROM Employee """ + clause
        employees = cursor.fetchall()
        cursor.close()
        return employees

    def selectEmployee(username, password):
        conn = dbapi.connect(url)
        cursor = conn.cursor()
        queryString = """
            SELECT EmployeeID, Username, Password, RoleID FROM Employee
            WHERE Username = '{}'
                AND Password = '{}'
        """.format(username, password)
        cursor.execute(queryString)
        employees = cursor.fetchone()
        cursor.close()
        return employees

    def deleteEmployee(employeeId):
        conn = dbapi.connect(url)
        cursor = conn.cursor()
        cursor.execute('UPDATE Employee SET IsActive = false WHERE EmployeeID = ' + employeeId)
        conn.commit()
        cursor.close()
        conn.close()

    def login(username, password):
        conn = dbapi.connect(url)
        cursor = conn.cursor()
        queryString = """
            SELECT EmployeeID, Username, Password FROM Employee
            WHERE Username = %s
                AND Password = %s
        """
        cursor.execute(queryString, (username, password))
        user = cursor.fetchone()
        cursor.close()
        if user != None:
            userId = user[0]
        else: return False
        return True

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

    def selectSystemValue(configID):
        conn = dbapi.connect(url)
        cursor = conn.cursor()
        queryString = """SELECT ConfigValue FROM System WHERE ConfigID = '{}'""".format(configID)
        cursor.execute(queryString)
        configItem = cursor.fetchone()
        cursor.close()
        return configItem

    def updateSystemEntry(configId, configValue, employeeId):
        conn = dbapi.connect(url)
        cursor = conn.cursor()
        queryString = """
            UPDATE System
                SET ConfigValue = '{}',
                    ModifiedOn = NOW(),
                    ModifiedBy = '{}'
                WHERE ConfigID = '{}' AND IsEditable = true
        """.format(configValue, employeeId, configId)
        cursor.execute(queryString)
        conn.commit()
        cursor.close()
        conn.close()

    def getSystemLogs():
        conn = dbapi.connect(url)
        cursor = conn.cursor()
        queryString = """
            SELECT LogID, Message, Page, LogType, Traceback, CreatedOn FROM Logs ORDER BY CreatedOn desc
        """
        cursor.execute(queryString)
        logs = cursor.fetchall()
        cursor.close()
        conn.close()
        return logs

    def insertLog(message, page, logType, traceback):
        conn = dbapi.connect(url)
        cursor = conn.cursor()
        queryString = """
            INSERT INTO Logs (Message, Page, LogType, Traceback, CreatedOn)
            VALUES (%s, %s, %s, %s, NOW())
        """
        cursor.execute(queryString, (message, page, logType, traceback))
        conn.commit()
        cursor.close()
        conn.close()
        
class Menu:
    def __init__(menuItemId, masterMenuItemId, permissionId, menuItemName, menuItemPath, iconPath, isActive, hasChildren):
        self.menuItemId = menuItemId
        self.masterMenuItemId = masterMenuItemId
        self.permissionId = permissionId
        self.menuItemName = menuItemName
        self.menuItemPath = menuItemPath
        self.iconPath = iconPath
        self.isActive = isActive
        self.hasChildren = hasChildren

    def selectMenuItems():
        conn = dbapi.connect(url)
        cursor = conn.cursor()
        queryString = """SELECT M.MenuItemID, M.MasterMenuItemID, M.PermissionID, L.Value, 
        M.MenuItemPath, M.IconPath, M.IsActive, M.HasChildren
        FROM Menu M
        INNER JOIN Localization L ON L.ResourceID = M.MenuItemName
        WHERE M.IsActive = true AND L.ResourceSet = 'Menu' AND L.LocaleID = 'tr'"""
        cursor.execute(queryString)
        menuItems = cursor.fetchall()
        cursor.close()
        return menuItems

class Permission:
    def __init__(permissionID, permissionCode, permissionName):
        self.permissionID = permissionID
        self.permissionCode = permissionCode
        self.permissionName = permissionName    

    def selectPermissions(roleID):
        conn = dbapi.connect(url)
        cursor = conn.cursor()
        queryString = """
            SELECT DISTINCT P.PermissionID, P.PermissionCode, P.PermissionName, 
            (RP.RoleID IS NULL) AS HasPermission FROM Permission P
            LEFT JOIN RolePermission RP ON RP.PermissionID = P.PermissionID
            WHERE RoleID = {}""".format(roleID)
        cursor.execute(queryString)
        permissions = cursor.fetchall()
        cursor.close()
        return permissions

    def hasPermission(roleID, permissionName):
        conn = dbapi.connect(url)
        cursor = conn.cursor()
        queryString = """
            SELECT RolePermissionID FROM RolePermission
            INNER JOIN Permission ON Permission.PermissionID = RolePermission.PermissionID
            WHERE RoleID = {}
                AND Permission.PermissionName = '{}'""".format(roleID, permissionName)

        cursor.execute(queryString)
        count = cursor.rowcount     
        cursor.close()

        if count == 0:
            return False
        else: return True

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

    def select():
        conn = dbapi.connect(url)
        cursor = conn.cursor()
        queryString = """SELECT ProductID, ProductTypeID, ProductName, Price, Calorie, Carbonhydrate, Fat, Glucose, IsVegetarian 
        FROM Product"""
        cursor.execute(queryString)
        products = cursor.fetchall()
        cursor.close()
        return products

class Localization:
    def __init__(pk, resourceID, localeID, resourceSet, value):
        self.pk = pk
        self.resourceID = resourceID
        self.localeID = localeID
        self.resourceSet = resourceSet
        self.value = value

    def selectLocalizationItem(resourceID, resourceSet, localeID):
        conn = dbapi.connect(url)
        cursor = conn.cursor()
        queryString = """SELECT Value FROM Localization 
            WHERE ResourceID = '{}' 
            AND ResourceSet = '{}'
            AND LocaleID = '{}'""".format(resourceID, resourceSet, localeID)
        cursor.execute(queryString)
        value = cursor.fetchone()
        return value

class RolePermission:
    def __init__(rolePermissionID, roleID, permissionID):
        self.rolePermissionID = rolePermissionID
        self.roleID = roleID
        self.permissionID = permissionID

    def select():
        conn = dbapi.connect(url)
        cursor = conn.cursor()
        queryString = """
            SELECT RoleID, PermissionID FROM RolePermission"""
        cursor.execute(queryString)
        rolePermissions = cursor.fetchall()
        cursor.close()
        return rolePermissions
    
    def insertPermissions(roleID, roleName, permissionList):
        conn = dbapi.connect(url)
        cursor = conn.cursor()
        if roleID != '':
            queryString = """DELETE FROM RolePermission WHERE RoleID = {}""".format(roleID)
            cursor.execute(queryString)
            queryString = """UPDATE Role
                             SET RoleName = %s
                             WHERE RoleID = %s"""
            cursor.execute(queryString, (roleName, roleID))
            for permission in permissionList:
                queryString = """INSERT INTO RolePermission (RoleID, PermissionID) VALUES({}, {})""".format(roleID, permission)
                cursor.execute(queryString)
        else:
            queryString = """INSERT INTO Role (RoleName, CreatedOn) VALUES (%s, NOW()) returning RoleID;"""
            cursor.execute(queryString, (roleName,))
            roleID = cursor.fetchone()
            for permission in permissionList:
                queryString = """INSERT INTO RolePermission (RoleID, PermissionID) VALUES({}, {})""".format(roleID[0], permission)
                cursor.execute(queryString)
        conn.commit()
        cursor.close()

    def selectRolePermissions(roleID):
        conn = dbapi.connect(url)
        cursor = conn.cursor()
        queryString = """
            SELECT
                Permission.PermissionID,
                Permission.PermissionName,
                CASE 
                    WHEN RolePermission.RolePermissionID IS NULL THEN
                        false
                    ELSE
                        true
                END AS Selected
            FROM Permission
            LEFT JOIN RolePermission ON RolePermission.PermissionID = Permission.PermissionID AND RolePermission.RoleID = {}
            """.format(roleID)
        cursor.execute(queryString)
        rolePermissions = cursor.fetchall()
        cursor.close()
        return rolePermissions

class Role:
    def __init__(roleID, roleName):
        self.roleID = roleID
        self.roleName = roleName

    def select():
        conn = dbapi.connect(url)
        cursor = conn.cursor()
        queryString = """
            SELECT RoleID, RoleName FROM Role"""
        cursor.execute(queryString)
        roles = cursor.fetchall()
        cursor.close()
        return roles
    
    def selectWithID(roleID):
        conn = dbapi.connect(url)
        cursor = conn.cursor()
        queryString = """
            SELECT RoleID, RoleName FROM Role WHERE RoleID = {}""".format(roleID)
        cursor.execute(queryString)
        if cursor.rowcount == 0:
            return tuple()
        role = cursor.fetchone()
        cursor.close()
        return role

class Sale:
    def __init__(saleID, employeeID, registerID, paymentMethod, createdOn, modifiedOn, isDelivered, isCancelled):
        self.saleID = saleID
        self.employeeID = employeeID
        self.registerID = registerID
        self.paymentMethod = paymentMethod
        self.createdOn = createdOn
        self.modifiedOn = modifiedOn
        self.isDelivered = isDelivered
        self.isCancelled = isCancelled

    def insert(employeeID, registerID, paymentMethod):
        conn = dbapi.connect(url)
        cursor = conn.cursor()
        queryString = """
            INSERT INTO Sale (EmployeeID, RegisterID, PaymentMethod, CreatedOn, ModifiedOn, IsDelivered. IsCancelled)
            VALUES ({}, {}, {}, NOW(), NULL, false, false)
        """.format(employeeID, registerID, paymentMethod)
        cursor.execute(queryString)
        connection.commit()
        cursor.close()

    def updateSale(saleID, isDelivered, isCancelled):
        conn = dbapi.connect(url)
        cursor = conn.cursor()
        queryString = """
            UPDATE Sale
                SET IsDelivered = {},
                    IsCancelled = {}
                WHERE SaleID = {}
        """.format(isDelivered, isCancelled, saleID)

    def getReportOnRegister(registerID):
        conn = dbapi.connect(url)
        cursor = conn.cursor()
        queryString = """
            SELECT E.Name + ' ' + E.Surname as FullName, R.RegisterID, R.RegisterTypeID,
            S.PaymentMethod, S.CreatedOn, S.ModifiedOn, S.IsDelivered, S.IsCancelled
            FROM Sale S
            INNER JOIN Employee E ON E.EmployeeID = S.EmployeeID
            INNER JOIN Register R ON R.RegisterID = S.RegisterID
            WHERE R.RegisterID = {}
        """.format(registerID)
        cursor.execute(queryString)
        report = cursor.fetchall()
        cursor.close()
        return report

    def getReportOnEmployee(employeeID):
        conn = dbapi.connect(url)
        cursor = conn.cursor()
        queryString = """
            SELECT E.Name + ' ' + E.Surname as FullName, R.RegisterID, R.RegisterTypeID,
            S.PaymentMethod, S.CreatedOn, S.ModifiedOn, S.IsDelivered, S.IsCancelled
            FROM Sale S
            INNER JOIN Employee E ON E.EmployeeID = S.EmployeeID
            INNER JOIN Register R ON R.RegisterID = S.RegisterID
            WHERE E.EmployeeID = {}
        """.format(employeeID)
        cursor.execute(queryString)
        report = cursor.fetchall()
        cursor.close()
        return report

    def getReport(registerID, employeeID):
        conn = dbapi.connect(url)
        cursor = conn.cursor()
        queryString = """
            SELECT E.Name + ' ' + E.Surname as FullName, R.RegisterID, R.RegisterTypeID,
            S.PaymentMethod, S.CreatedOn, S.ModifiedOn, S.IsDelivered, S.IsCancelled
            FROM Sale S
            INNER JOIN Employee E ON E.EmployeeID = S.EmployeeID
            INNER JOIN Register R ON R.RegisterID = S.RegisterID
            WHERE E.EmployeeID = {} AND R.RegisterID = {}
        """.format(employeeID, registerID)
        cursor.execute(queryString)
        report = cursor.fetchall()
        cursor.close()
        return report

class Register:
    def __init__(registerID, registerTypeID, isActive):
        self.registerID = registerID
        self.registerTypeID = registerTypeID
        self.isActive = isActive

    def select():
        conn = dbapi.connect(url)
        cursor = conn.cursor()
        queryString = """
            SELECT
            Register.RegisterID,
            RegisterType.RegisterTypeName
            FROM Register
            INNER JOIN RegisterType ON RegisterType.RegisterTypeID = Register.RegisterTypeID
            WHERE Register.IsActive = true
        """
        cursor.execute(queryString)
        registers = cursor.fetchall()
        cursor.close()
        return registers
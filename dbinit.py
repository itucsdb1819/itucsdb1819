import os
import sys
import psycopg2 as dbapi2

INIT_STATEMENTS = [
	"DROP TABLE IF EXISTS Localization",
	"DROP TABLE IF EXISTS Menu",
	"DROP TABLE IF EXISTS IngredientType CASCADE",
	"DROP TABLE IF EXISTS Ingredient CASCADE",
	"DROP TABLE IF EXISTS Toy CASCADE",
	"DROP TABLE IF EXISTS FoodMenu CASCADE",
	"DROP TABLE IF EXISTS ProductType CASCADE",
	"DROP TABLE IF EXISTS Product CASCADE",
	"DROP TABLE IF EXISTS ProductMenu CASCADE",
	"DROP TABLE IF EXISTS ProductIngredient CASCADE",
	"DROP TABLE IF EXISTS RegisterType CASCADE",
	"DROP TABLE IF EXISTS Register CASCADE",
	"DROP TABLE IF EXISTS Title CASCADE",
	"DROP TABLE IF EXISTS Permission CASCADE",
	"DROP TABLE IF EXISTS Role CASCADE",
	"DROP TABLE IF EXISTS RolePermission CASCADE",
	"DROP TABLE IF EXISTS Employee CASCADE",
	"DROP TABLE IF EXISTS System CASCADE",
	"DROP TABLE IF EXISTS Expense CASCADE",
	"DROP TABLE IF EXISTS Sale CASCADE",
	"DROP TABLE IF EXISTS CustomerSurvey CASCADE",
	"DROP TABLE IF EXISTS ProductSale CASCADE",

"""CREATE TABLE IF NOT EXISTS Localization(
	PK serial PRIMARY KEY,
	ResourceId varchar(50) NOT NULL, 
	LocaleId varchar(4) NOT NULL, 
	ResourceSet varchar(50) NOT NULL, 
	Value varchar(50) NOT NULL
)""",
"""CREATE TABLE IF NOT EXISTS Menu(
	MenuItemID integer PRIMARY KEY,
	MasterMenuItemID integer NULL REFERENCES Menu (MenuItemID),
	PermissionID integer NULL,
	MenuItemName varchar(50) NOT NULL, 
	MenuItemPath varchar(50) NOT NULL, 
	IconPath varchar(50) NOT NULL, 
	IsActive bool NOT NULL,
	HasChildren bool NOT NULL
)""",
"""CREATE TABLE IF NOT EXISTS IngredientType(
	IngredienTypeID integer PRIMARY KEY,
	IngredientTypeName varchar(50) NOT NULL
)""",
"""CREATE TABLE IF NOT EXISTS Ingredient(
	IngredientID integer REFERENCES IngredientType,
	IngredienTypeID integer NOT NULL,
	IngredientName varchar(50) NOT NULL,
	PRIMARY KEY (IngredientID)
)""",
"""CREATE TABLE IF NOT EXISTS Toy(
	ToyID serial PRIMARY KEY,
	ToyName varchar(50) NOT NULL, 
	Promotion text NOT NULL, 
	CreatedOn timestamp NOT NULL 
)""",
"""CREATE TABLE IF NOT EXISTS FoodMenu(
	FoodMenuID serial PRIMARY KEY,
	ToyID integer NULL REFERENCES Toy,
	Discount decimal NOT NULL, 
	IsActive bool NOT NULL, 
	IsChildrenOnly bool NOT NULL, 
	CreatedOn timestamp NOT NULL, 
	ModifiedOn timestamp NULL
)""",
"""CREATE TABLE IF NOT EXISTS ProductType(
	ProductTypeID integer PRIMARY KEY,
	ProductTypeName varchar(50) NOT NULL
)""",
"""CREATE TABLE IF NOT EXISTS Product(
	ProductID serial PRIMARY KEY,
	ProductTypeID integer NOT NULL REFERENCES ProductType,
	ProductName varchar(50) NOT NULL, 
	Price decimal NOT NULL, 
	Calorie decimal NOT NULL, 
	Protein decimal NOT NULL, 
	Carbonhydrate decimal NOT NULL, 
	Fat decimal NOT NULL, 
	Glucose decimal NOT NULL, 
	IsVegetarian bool NOT NULL
)""",
"""CREATE TABLE IF NOT EXISTS ProductMenu(
	ProductMenuID serial REFERENCES FoodMenu,
	FoodMenuID integer NOT NULL,
	ProductID integer NOT NULL REFERENCES Product,
	PRIMARY KEY (ProductMenuID)
)""",
"""CREATE TABLE IF NOT EXISTS ProductIngredient(
	ProductIngredientID serial PRIMARY KEY,
	ProductID integer NOT NULL REFERENCES Product,
	IngredientID integer NOT NULL REFERENCES Ingredient
)""",
"""CREATE TABLE IF NOT EXISTS RegisterType(
	RegisterTypeID integer PRIMARY KEY,
	RegisterTypeName varchar(50) NOT NULL
)""",
"""CREATE TABLE IF NOT EXISTS Register(
	RegisterID integer REFERENCES RegisterType,
	RegisterTypeID integer NOT NULL,
	IsActive bool NOT NULL,
	PRIMARY KEY (RegisterID)
)""",
"""CREATE TABLE IF NOT EXISTS Title(
	TitleID serial PRIMARY KEY,
	TitleName varchar(50) NOT NULL, 
	MonthlyPay decimal NOT NULL, 
	ModifiedOn timestamp NULL
)""",
"""CREATE TABLE IF NOT EXISTS Permission(
	PermissionID integer PRIMARY KEY,
	PermissionName varchar(50) NOT NULL
)""",
"""CREATE TABLE IF NOT EXISTS Role(
	RoleID serial PRIMARY KEY,
	RoleName varchar(50) NOT NULL, 
	CreatedOn timestamp NOT NULL, 
	ModifiedOn timestamp NULL
)""",
"""CREATE TABLE IF NOT EXISTS RolePermission(
	RolePermissionID serial PRIMARY KEY,
	RoleID integer NOT NULL REFERENCES Role,
	PermissionID integer NOT NULL REFERENCES Permission
)""",
"""CREATE TABLE IF NOT EXISTS Employee(
	EmployeeID serial PRIMARY KEY,
	RoleID integer NOT NULL REFERENCES Role,
	Name varchar(50) NOT NULL, 
	Surname varchar(50) NOT NULL, 
	CreatedOn timestamp NOT NULL, 
	ModifiedOn timestamp NULL, 
	IsActive bool NOT NULL, 
	TitleID integer NOT NULL REFERENCES Title,
	Username varchar(50),
	Password text
)""",
"""CREATE TABLE IF NOT EXISTS System(
	ConfigId varchar(50) PRIMARY KEY,
	ConfigValue varchar(50) NOT NULL, 
	ConfigValueType varchar(50) NOT NULL, 
	IsEditable bool NOT NULL, 
	CreatedOn timestamp NOT NULL, 
	ModifiedOn timestamp NULL, 
	ModifiedBy integer NULL REFERENCES Employee (EmployeeID)
)""",
"""CREATE TABLE IF NOT EXISTS Expense(
	ExpenseID serial PRIMARY KEY,
	Amount decimal NOT NULL, 
	Description varchar(50) NOT NULL, 
	CreatedOn timestamp NOT NULL, 
	ModifiedOn timestamp NULL, 
	IsPremium bool NOT NULL, 
	CreatedBy integer NOT NULL REFERENCES Employee (EmployeeID),
	ModifiedBy integer NULL REFERENCES Employee (EmployeeID)
)""",
"""CREATE TABLE IF NOT EXISTS Sale(
	SaleID serial PRIMARY KEY,
	EmployeeID integer NULL REFERENCES Employee,
	RegisterID integer NOT NULL REFERENCES Register,
	PaymentMethod varchar(50) NOT NULL, 
	CreatedOn timestamp NOT NULL, 
	ModifiedOn timestamp NULL, 
	IsDelivered bool NULL, 
	IsCancelled bool NULL 
)""",
"""CREATE TABLE IF NOT EXISTS CustomerSurvey(
	SurveyID serial PRIMARY KEY,
	SaleID integer NOT NULL REFERENCES Sale,
	SurveyGUID text NOT NULL, 
	Score decimal NOT NULL, 
	CustomerAddition text NULL, 
	CreatedOn timestamp NOT NULL, 
	CompletedOn timestamp NULL, 
	IsSurveyCodeExpired bool NOT NULL
)""",
"""CREATE TABLE IF NOT EXISTS ProductSale(
	ProductSaleID serial PRIMARY KEY,
	ProductID integer NOT NULL REFERENCES Product,
	SaleID integer NOT NULL REFERENCES Sale,
	Note text NULL 
)""",
"""CREATE TABLE IF NOT EXISTS Logs(
	LogID serial PRIMARY KEY,
	Message text NOT NULL,
	Page text NOT NULL
	Type text NOT NULL
	Traceback text NOT NULL,
	CreatedOn timestamp NOT NULL
)"""
]

TITLE_INSERT_STATEMENTS = [
	"""INSERT INTO Title (TitleName, MonthlyPay)
	VALUES ('Cashier', 1457)"""
]


LOCALIZATION_INSERT_STATEMENTS = [
	"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Menu.Home', 'Menu', 'tr', 'Anasayfa')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Menu.Administration', 'Menu', 'tr', 'Yönetim')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Menu.Accounting', 'Menu', 'tr', 'Muhasebe')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Menu.SystemConfiguration', 'Menu', 'tr', 'Sistem Ayarları')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Menu.Employee', 'Menu', 'tr', 'Çalışanlar')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Menu.RoleAndPermissions', 'Menu', 'tr', 'Roller ve İzinler')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Menu.Expense', 'Menu', 'tr', 'Masraflar')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Menu.Product', 'Menu', 'tr', 'Ürünler')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Menu.SalesReport', 'Menu', 'tr', 'Satış Raporu')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Employee.Create', 'PageText', 'tr', 'Çalışan Ekle')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Login.Login', 'PageText', 'tr', 'Giriş Yap')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Employee', 'PageTitles', 'tr', 'Çalışanlar')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('RolesAndPermissions', 'PageTitles', 'tr', 'Roller ve İzinler')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Button.Edit', 'Buttons', 'tr', 'Düzenle')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Admin', 'PageText', 'tr', 'Yönetici')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Accounting', 'PageText', 'tr', 'Muhasebe')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Button.Save', 'Buttons', 'tr', 'Kaydet')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('HomePage.Return', 'Buttons', 'tr', 'Anasayfa')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Error.UnauthorizedAccess', 'PageTitles', 'tr', 'İzinsiz erişim!')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Error.UnauthorizedAccess', 'PageText', 'tr', 'İzinsiz erişim sağladınız.')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Error.InvalidCredentials', 'PageText', 'tr', 'Kullanıcı adı veya şifre hatalı.')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Error.InternalServerError', 'PageTitles', 'tr', 'Sunucu hatası!')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Error.InternalServerError', 'PageText', 'tr', 'Sunucu hatası meydana geldi.')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Error.SessionExpired', 'PageText', 'tr', 'Giriş yapmanız gerekmektedir.')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Expense', 'PageTitles', 'tr', 'Masraflar')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('HomePage.Access', 'PageText', 'tr', 'Anasayfa Erişim İzni.')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('EmployeePage.Access', 'PageText', 'tr', 'Çalışanlar Sayfası Erişim İzni.')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('ExpensePage.Access', 'PageText', 'tr', 'Masraflar Sayfası Erişim İzni.')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('RolesAndPermissionsPage.Access', 'PageText', 'tr', 'Roller ve İzinler Sayfası Erişim İzni.')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('ProductPage.Access', 'PageText', 'tr', 'Ürünler Sayfası Erişim İzni.')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('SalesPage.Access', 'PageText', 'tr', 'Satışlar Sayfası Erişim İzni.')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('SystemPage.Access', 'PageText', 'tr', 'Sistem Ayarları Sayfası Erişim İzni.')""",
]

ROLE_INSERT_STATEMENTS = [
"""
	INSERT INTO Role(RoleName, CreatedOn)
	VALUES ('Admin', NOW())
""",
"""
	INSERT INTO Role(RoleName, CreatedOn)
	VALUES ('Accounting', NOW())
""",
]

PERMISSION_INSERT_STATEMENTS = [
	"""
		INSERT INTO Permission (PermissionID, PermissionName)
		VALUES (1, 'HomePage.Access')
	""",
	"""
		INSERT INTO Permission (PermissionID, PermissionName)
		VALUES (2, 'EmployeePage.Access')
	""",
	"""
		INSERT INTO Permission (PermissionID, PermissionName)
		VALUES (3, 'RolesAndPermissionsPage.Access')
	""",
	"""
		INSERT INTO Permission (PermissionID, PermissionName)
		VALUES (4, 'ExpensePage.Access')
	""",
	"""
		INSERT INTO Permission (PermissionID, PermissionName)
		VALUES (5, 'ProductPage.Access')
	""",
	"""
		INSERT INTO Permission (PermissionID, PermissionName)
		VALUES (6, 'SalesPage.Access')
	""",
	"""
		INSERT INTO Permission (PermissionID, PermissionName)
		VALUES (7, 'SystemPage.Access')
	"""
]

ROLE_PERMISSION_INSERT_STATEMENTS = [
	"""
		INSERT INTO RolePermission(RoleID, PermissionID)
		VALUES (1, 1)
	""",
	"""
		INSERT INTO RolePermission(RoleID, PermissionID)
		VALUES (1, 2)
	""",
	"""
		INSERT INTO RolePermission(RoleID, PermissionID)
		VALUES (1, 3)
	""",
	"""
		INSERT INTO RolePermission(RoleID, PermissionID)
		VALUES (1, 4)
	""",
	"""
		INSERT INTO RolePermission(RoleID, PermissionID)
		VALUES (1, 5)
	""",
	"""
		INSERT INTO RolePermission(RoleID, PermissionID)
		VALUES (1, 6)
	"""
]

EMPLOYEE_INSERT_STATEMENTS = [
"""
	INSERT INTO Employee (RoleID, Name, Surname, CreatedOn, IsActive, TitleID, Username, Password)
	VALUES (1, 'Merve', 'Donmez', NOW(), true, 1, 'mgdonmez', 'superpass')
"""
]

MENU_INSERT_STATEMENTS = [
"""INSERT INTO Menu (MenuItemID, MasterMenuItemID, PermissionID, MenuItemName, MenuItemPath, IconPath, IsActive, HasChildren)
	VALUES (1, NULL, 1, 'Menu.Home', '/', 'fa fa-home', true, false)
""",
"""INSERT INTO Menu (MenuItemID, MasterMenuItemID, PermissionID, MenuItemName, MenuItemPath, IconPath, IsActive, HasChildren)
	VALUES (2, NULL, NULL, 'Menu.Administration', '#', 'fa fa-user-circle', true, true)
""",
"""INSERT INTO Menu (MenuItemID, MasterMenuItemID, PermissionID, MenuItemName, MenuItemPath, IconPath, IsActive, HasChildren)
	VALUES (3, NULL, NULL, 'Menu.Accounting', '#', 'fa fa-calculator', true, true)
""",
"""INSERT INTO Menu (MenuItemID, MasterMenuItemID, PermissionID, MenuItemName, MenuItemPath, IconPath, IsActive, HasChildren)
	VALUES (4, NULL, 7, 'Menu.SystemConfiguration', '/system', 'fa fa-cogs', true, false)
""",
"""INSERT INTO Menu (MenuItemID, MasterMenuItemID, PermissionID, MenuItemName, MenuItemPath, IconPath, IsActive, HasChildren)
	VALUES (5, 2, 2, 'Menu.Employee', '/employee', '', true, false)
""",
"""INSERT INTO Menu (MenuItemID, MasterMenuItemID, PermissionID, MenuItemName, MenuItemPath, IconPath, IsActive, HasChildren)
	VALUES (6, 2, 3, 'Menu.RoleAndPermissions', '/roles_and_permissions', '', true, false)
""",
"""INSERT INTO Menu (MenuItemID, MasterMenuItemID, PermissionID, MenuItemName, MenuItemPath, IconPath, IsActive, HasChildren)
	VALUES (7, 3, 4, 'Menu.Expense', '/expense', '', true, false)
""",
"""INSERT INTO Menu (MenuItemID, MasterMenuItemID, PermissionID, MenuItemName, MenuItemPath, IconPath, IsActive, HasChildren)
	VALUES (8, 3, 5, 'Menu.Product', '/product', '', true, false)
""",
"""INSERT INTO Menu (MenuItemID, MasterMenuItemID, PermissionID, MenuItemName, MenuItemPath, IconPath, IsActive, HasChildren)
	VALUES (9, 3, 6, 'Menu.SalesReport', '/sales', '', true, false)
"""
]

SYSTEM_INSERT_STATEMENTS = [
	"""INSERT INTO System (ConfigId, ConfigValue, ConfigValueType, IsEditable, CreatedOn, ModifiedOn, ModifiedBy)
	VALUES ('SystemLanguage', 'tr', 'string', true, NOW(), NULL, NULL)""",
	"""INSERT INTO System (ConfigId, ConfigValue, ConfigValueType, IsEditable, CreatedOn, ModifiedOn, ModifiedBy)
	VALUES ('Currency', 'TL', 'string', true, NOW(), NULL, NULL)""",
]

PRODUCT_TYPE_INSERT_STATEMENTS = [
	"""
		INSERT INTO ProductType (ProductTypeID, ProductTypeName)
						 VALUES (1, 'ProductType.Single')
	""",
	"""
		INSERT INTO ProductType (ProductTypeID, ProductTypeName)
						 VALUES (2, 'ProductType.Drink')
	""",
	"""
		INSERT INTO ProductType (ProductTypeID, ProductTypeName)
						 VALUES (3, 'ProductType.Dessert')
	""",
	"""
		INSERT INTO ProductType (ProductTypeID, ProductTypeName)
						 VALUES (4, 'ProductType.LightAndActive')
	""",
	"""
		INSERT INTO ProductType (ProductTypeID, ProductTypeName)
						 VALUES (5, 'ProductType.Breakfast')
	"""
]

PRODUCT_INSERT_STATEMENTS = [
	"""
		INSERT INTO Product (ProductTypeID, ProductName, Price, Calorie, Protein, Carbonhydrate, Fat, Glucose, IsVegetarian)
					 VALUES (1, 'Product.Hamburger', 0, 250, 14, 31, 8, 6, false)
	""",
	"""
		INSERT INTO Product (ProductTypeID, ProductName, Price, Calorie, Protein, Carbonhydrate, Fat, Glucose, IsVegetarian)
					 VALUES (1, 'Product.FrenchFriesMedium', 0, 280, 4, 37, 13, 0, false)
	""",
	"""
		INSERT INTO Product (ProductTypeID, ProductName, Price, Calorie, Protein, Carbonhydrate, Fat, Glucose, IsVegetarian)
					 VALUES (2, 'Product.CocaCola250', 0, 113, 0, 28, 0, 28, false)
	"""
]

def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)

        for statement in MENU_INSERT_STATEMENTS:
            cursor.execute(statement)

        for statement in SYSTEM_INSERT_STATEMENTS:
            cursor.execute(statement)	

        for statement in TITLE_INSERT_STATEMENTS:
            cursor.execute(statement)        
        
        for statement in LOCALIZATION_INSERT_STATEMENTS:
            cursor.execute(statement)

        for statement in PRODUCT_TYPE_INSERT_STATEMENTS:
            cursor.execute(statement)

        for statement in PRODUCT_INSERT_STATEMENTS:
            cursor.execute(statement)

        for statement in ROLE_INSERT_STATEMENTS:
            cursor.execute(statement)

        for statement in TITLE_INSERT_STATEMENTS:
            cursor.execute(statement)

        for statement in EMPLOYEE_INSERT_STATEMENTS:
            cursor.execute(statement)

        for statement in PERMISSION_INSERT_STATEMENTS:
            cursor.execute(statement)

        for statement in ROLE_PERMISSION_INSERT_STATEMENTS:
            cursor.execute(statement)

        connection.commit()
        cursor.close()

if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stdout)
        sys.exit(1)
    initialize(url)

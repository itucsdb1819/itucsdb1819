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
	IsActive bool NOT NULL
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
	Carbohydrate decimal NOT NULL, 
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
	PermissionCode varchar(50) NOT NULL,
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
)"""
]

TITLE_INSERT_STATEMENTS = []

ROLE_INSERT_STATEMENTS = []

PERMISSION_INSERT_STATEMENTS = []

ROLE_PERMISSION_ONSERT_STATEMENTS = []

EMPLOYEE_INSERT_STATEMENTS = []

MENU_INSERT_STATEMENTS = [
"""INSERT INTO Menu (MenuItemID, MasterMenuItemID, PermissionID, MenuItemName, MenuItemPath, IconPath, IsActive)
	VALUES (1, NULL, NULL, 'Menu.Home', '/', 'fa fa-home', true)
""",
"""INSERT INTO Menu (MenuItemID, MasterMenuItemID, PermissionID, MenuItemName, MenuItemPath, IconPath, IsActive)
	VALUES (2, NULL, NULL, 'Menu.Administration', '#', '', true)
""",
"""INSERT INTO Menu (MenuItemID, MasterMenuItemID, PermissionID, MenuItemName, MenuItemPath, IconPath, IsActive)
	VALUES (3, NULL, NULL, 'Menu.Accounting', '#', '', true)
""",
"""INSERT INTO Menu (MenuItemID, MasterMenuItemID, PermissionID, MenuItemName, MenuItemPath, IconPath, IsActive)
	VALUES (4, NULL, NULL, 'Menu.SystemConfiguration', '/system', '', true)
""",
"""INSERT INTO Menu (MenuItemID, MasterMenuItemID, PermissionID, MenuItemName, MenuItemPath, IconPath, IsActive)
	VALUES (5, 2, NULL, 'Menu.Employee', '/employee', '', true)
""",
"""INSERT INTO Menu (MenuItemID, MasterMenuItemID, PermissionID, MenuItemName, MenuItemPath, IconPath, IsActive)
	VALUES (6, 2, NULL, 'Menu.RoleAndPermissions', '/roles_and_permissions', '', true)
""",
"""INSERT INTO Menu (MenuItemID, MasterMenuItemID, PermissionID, MenuItemName, MenuItemPath, IconPath, IsActive)
	VALUES (7, 3, NULL, 'Menu.Expense', '/expense', '', true)
""",
"""INSERT INTO Menu (MenuItemID, MasterMenuItemID, PermissionID, MenuItemName, MenuItemPath, IconPath, IsActive)
	VALUES (8, 3, NULL, 'Menu.Product', '/product', '', true)
""",
"""INSERT INTO Menu (MenuItemID, MasterMenuItemID, PermissionID, MenuItemName, MenuItemPath, IconPath, IsActive)
	VALUES (9, 3, NULL, 'Menu.SalesReport', '/sales_report', '', true)
"""
]

SYSTEM_INSERT_STATEMENTS = [
	"""INSERT INTO System (ConfigId, ConfigValue, ConfigValueType, IsEditable, CreatedOn, ModifiedOn, ModifiedBy)
	VALUES ('SystemLanguage', 'tr', 'string', true, NOW(), NULL, NULL)""",
	"""INSERT INTO System (ConfigId, ConfigValue, ConfigValueType, IsEditable, CreatedOn, ModifiedOn, ModifiedBy)
	VALUES ('Currency', 'TL', 'string', true, NOW(), NULL, NULL)""",
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            print(statement)
            cursor.execute(statement)

		for statement in MENU_INSERT_STATEMENTS:
            print(statement)
            cursor.execute(statement)

		for statement in SYSTEM_INSERT_STATEMENTS:
            print(statement)
            cursor.execute(statement)	

        connection.commit()
        cursor.close()

if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stdout)
        sys.exit(1)
    initialize(url)

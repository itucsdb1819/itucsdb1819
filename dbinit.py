import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
	"DROP TABLE IF EXISTS Localization",
	"DROP TABLE IF EXISTS Menu",
	"DROP TABLE IF EXISTS IngredientType",
	"DROP TABLE IF EXISTS Ingredient",
	"DROP TABLE IF EXISTS Toy",
	"DROP TABLE IF EXISTS FoodMenu",
	"DROP TABLE IF EXISTS ProductType",
	"DROP TABLE IF EXISTS Product",
	"DROP TABLE IF EXISTS ProductMenu",
	"DROP TABLE IF EXISTS ProductIngredient",
	"DROP TABLE IF EXISTS RegisterType",
	"DROP TABLE IF EXISTS Register",
	"DROP TABLE IF EXISTS Title",
	"DROP TABLE IF EXISTS Permission",
	"DROP TABLE IF EXISTS Role",
	"DROP TABLE IF EXISTS RolePermission",
	"DROP TABLE IF EXISTS Employee",
	"DROP TABLE IF EXISTS System",
	"DROP TABLE IF EXISTS Expense",
	"DROP TABLE IF EXISTS Sale",
	"DROP TABLE IF EXISTS CustomerSurvey",
	"DROP TABLE IF EXISTS ProductSale",

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
	PermissionID integer NOT NULL,
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
	Username varchar(50) NOT NULL,
	Password text NOT NULL
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


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        connection.commit()
        cursor.close()

if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)

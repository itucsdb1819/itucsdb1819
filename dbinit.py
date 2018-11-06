import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
"""CREATE TABLE IF NOT EXISTS CustomerSurvey(
	SurveyID int PRIMARY KEY,
	SaleID int NOT NULL,
	SurveyGUID text NOT NULL, 
	Score decimal NOT NULL, 
	CustomerAddition text NULL, 
	CreatedOn timestamp NOT NULL, 
	CompletedOn timestamp NULL, 
	IsSurveyCodeExpired bool NOT NULL
)""",
"""CREATE TABLE IF NOT EXISTS Employee(
	EmployeeID int SERIAL PRIMARY KEY,
	RoleID int NOT NULL,
	Name varchar(50) NOT NULL, 
	Surname varchar(50) NOT NULL, 
	CreatedOn timestamp NOT NULL, 
	ModifiedOn timestamp NULL, 
	IsActive bool NOT NULL, 
	TitleID int NOT NULL
)""",
"""CREATE TABLE IF NOT EXISTS Expense(
	ExpenseID int SERIAL PRIMARY KEY,
	Amount decimal NOT NULL, 
	Description varchar(50) NOT NULL, 
	CreatedOn timestamp NOT NULL, 
	ModifiedOn timestamp NULL, 
	IsPremium bool NOT NULL, 
	CreatedBy int NOT NULL,
	ModifiedBy int NULL
)""",
"""CREATE TABLE IF NOT EXISTS FoodMenu(
	FoodMenuID int SERIAL PRIMARY KEY,
	ToyID int NULL,
	Discount decimal NOT NULL, 
	IsActive bool NOT NULL, 
	IsChildrenOnly bool NOT NULL, 
	CreatedOn timestamp NOT NULL, 
	ModifiedOn timestamp NULL
)""",
"""CREATE TABLE IF NOT EXISTS Ingredient(
	IngredientID int PRIMARY KEY,
	IngredienTypeID int NOT NULL,
	IngredientName varchar(50) NOT NULL
)""",
"""CREATE TABLE IF NOT EXISTS IngredientType(
	IngredienTypeID int PRIMARY KEY,
	IngredientTypeName varchar(50) NOT NULL
)""",
"""CREATE TABLE IF NOT EXISTS Localization(
	PK int SERIAL PRIMARY KEY,
	ResourceId varchar(50) NOT NULL, 
	LocaleId varchar(4) NOT NULL, 
	ResourceSet varchar(50) NOT NULL, 
	Value varchar(50) NOT NULL
)""",
"""CREATE TABLE IF NOT EXISTS Menu(
	MenuItemID int PRIMARY KEY,
	MasterMenuItemID int NULL,
	PermissionID int NOT NULL,
	MenuItemName varchar(50) NOT NULL, 
	MenuItemPath varchar(50) NOT NULL, 
	IconPath varchar(50) NOT NULL, 
	IsActive bool NOT NULL
	)""",
"""CREATE TABLE IF NOT EXISTS Permission(
	PermissionID int PRIMARY KEY,
	PermissionCode varchar(50) NOT NULL,
	PermissionName varchar(50) NOT NULL
)""",
"""CREATE TABLE IF NOT EXISTS Product(
	ProductID int SERIAL PRIMARY KEY,
	ProductTypeID int NOT NULL,
	ProductName varchar(50) NOT NULL, 
	Price decimal NOT NULL, 
	Calorie decimal NOT NULL, 
	Protein decimal NOT NULL, 
	Carbohydrate decimal NOT NULL, 
	Fat decimal NOT NULL, 
	Glucose decimal NOT NULL, 
	IsVegetarian bool NOT NULL
)""",
"""CREATE TABLE IF NOT EXISTS ProductIngredient(
	ProductIngredientID int SERIAL PRIMARY KEY,
	ProductID int NOT NULL,
	IngredientID int NOT NULL
)""",
"""CREATE TABLE IF NOT EXISTS ProductMenu(
	ProductMenuID int SERIAL PRIMARY KEY,
	FoodMenuID int NOT NULL,
	ProductID int NOT NULL
)""",
"""CREATE TABLE IF NOT EXISTS ProductSale(
	ProductSaleID int SERIAL PRIMARY KEY,
	ProductID int NOT NULL,
	SaleID int NOT NULL,
	Note text NULL 
)""",
"""CREATE TABLE IF NOT EXISTS ProductType(
	ProductTypeID int PRIMARY KEY,
	ProductTypeName varchar(50) NOT NULL
)""",
"""CREATE TABLE IF NOT EXISTS Register(
	RegisterID int PRIMARY KEY,
	RegisterTypeID int NOT NULL,
	IsActive bool NOT NULL
)""",
"""CREATE TABLE IF NOT EXISTS RegisterType(
	RegisterTypeID int PRIMAY KEY,
	RegisterTypeName varchar(50) NOT NULL
)""",
"""CREATE TABLE IF NOT EXISTS Role(
	RoleID int SERIAL PRIMARY KEY,
	RoleName varchar(50) NOT NULL, 
	CreatedOn timestamp NOT NULL, 
	ModifiedOn timestamp NULL, 
	CreatedBy int NOT NULL,
	ModifiedBy int NULL
)""",
"""CREATE TABLE IF NOT EXISTS RolePermission(
	RolePermissionID int SERIAL PRIMARY KEY,
	RoleID int NOT NULL,
	PermissionID int NOT NULL,
CONSTRAINT IX_RolePermission UNIQUE NONCLUSTERED 
(
	PermissionID,
	RoleID
))""",
"""CREATE TABLE IF NOT EXISTS Sale(
	SaleID int SERIAL PRIMARY KEY,
	EmployeeID int NULL,
	RegisterID int NOT NULL,
	SurveyID int NOT NULL,
	PaymentMethod varchar(50) NOT NULL, 
	CreatedOn timestamp NOT NULL, 
	ModifiedOn timestamp NULL, 
	IsDelivered bool NULL, 
	IsCancelled bool NULL 
)""",
"""CREATE TABLE IF NOT EXISTS System(
	ConfigId varchar(50) PRIMAY KEY,
	ConfigValue varchar(50) NOT NULL, 
	ConfigValueType varchar(50) NOT NULL, 
	IsEditable bool NOT NULL, 
	CreatedOn timestamp NOT NULL, 
	ModifiedOn timestamp NULL, 
	ModifiedBy int NULL
)""",
"""CREATE TABLE IF NOT EXISTS Title(
	TitleID int SERIAL PRIMARY KEY,
	TitleName varchar(50) NOT NULL, 
	MonthlyPay decimal NOT NULL, 
	ModifiedOn timestamp NULL
)""",
"""CREATE TABLE IF NOT EXISTS Toy(
	ToyID int SERIAL PRIMARY KEY,
	ToyName varchar(50) NOT NULL, 
	Promotion text NOT NULL, 
	CreatedOn timestamp NOT NULL 
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

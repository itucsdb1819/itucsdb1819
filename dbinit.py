import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
    """CREATE TABLE IF NOT EXISTS CustomerSurvey(
	SurveyID int NOT NULL,
	SaleID int NOT NULL,
	SurveyGUID nvarchar(max) NOT NULL, 
	Score decimal(18, 2) NOT NULL, 
	CustomerAddition nvarchar(max) NULL, 
	CreatedOn datetime NOT NULL, 
	CompletedOn datetime NULL, 
	IsSurveyCodeExpired bit NOT NULL, 
	PRIMARY KEY (SurveyID)
	""",
    """CREATE TABLE IF NOT EXISTS Employee(
	EmployeeID int SERIAL PRIMARY KEY NOT NULL,
	RoleID int NOT NULL,
	Name nvarchar(50) NOT NULL, 
	Surname nvarchar(50) NOT NULL, 
	CreatedOn datetime NOT NULL, 
	ModifiedOn datetime NULL, 
	IsActive bit NOT NULL, 
	TitleID int NOT NULL
""",
"""CREATE TABLE IF NOT EXISTS Expense(
	ExpenseID int SERIAL PRIMARY KEY NOT NULL,
	Amount decimal(18, 2) NOT NULL, 
	Description nvarchar(50) NOT NULL, 
	CreatedOn datetime NOT NULL, 
	ModifiedOn datetime NULL, 
	IsPremium bit NOT NULL, 
	CreatedBy int NOT NULL,
	ModifiedBy int NULL
""",
"""CREATE TABLE IF NOT EXISTS FoodMenu(
	FoodMenuID int SERIAL PRIMARY KEY NOT NULL,
	ToyID int NULL,
	Discount decimal(18, 2) NOT NULL, 
	IsActive bit NOT NULL, 
	IsChildrenOnly bit NOT NULL, 
	CreatedOn datetime NOT NULL, 
	ModifiedOn datetime NULL
""",
"""CREATE TABLE IF NOT EXISTS Ingredient(
	IngredientID int NOT NULL,
	IngredienTypeID int NOT NULL,
	IngredientName nvarchar(50) NOT NULL,
	PRIMARY KEY (IngredientID) 
""",
"""CREATE TABLE IF NOT EXISTS IngredientType(
	IngredienTypeID int NOT NULL,
	IngredientTypeName nvarchar(50) NOT NULL, 
    PRIMARY KEY (IngredientTypeID)
""",
"""CREATE TABLE IF NOT EXISTS Localization(
	PK int SERIAL PRIMARY KEY NOT NULL,
	ResourceId nvarchar(50) NOT NULL, 
	LocaleId varchar(4) NOT NULL, 
	ResourceSet nvarchar(50) NOT NULL, 
	Value nvarchar(50) NOT NULL
""",
"""CREATE TABLE IF NOT EXISTS Menu(
	MenuItemID int NOT NULL,
	MasterMenuItemID int NULL,
	PermissionID int NOT NULL,
	MenuItemName nvarchar(50) NOT NULL, 
	MenuItemPath nvarchar(50) NOT NULL, 
	IconPath nvarchar(50) NOT NULL, 
	IsActive bit NOT NULL,
	PRIMARY KEY (MenuItemID)
	""",
"""CREATE TABLE IF NOT EXISTS Permission(
	PermissionID int NOT NULL,
	PermissionCode nvarchar(50) NOT NULL,
	PermissionName nvarchar(50) NOT NULL, 
	PRIMARY KEY (PermissionID)
""",
"""CREATE TABLE IF NOT EXISTS Product(
	ProductID int SERIAL PRIMARY KEY NOT NULL,
	ProductTypeID int NOT NULL,
	ProductName nvarchar(50) NOT NULL, 
	Price decimal(18, 2) NOT NULL, 
	Calorie decimal(18, 2) NOT NULL, 
	Protein decimal(18, 2) NOT NULL, 
	Carbohydrate decimal(18, 2) NOT NULL, 
	Fat decimal(18, 2) NOT NULL, 
	Glucose decimal(18, 2) NOT NULL, 
	IsVegetarian bit NOT NULL
""",
"""CREATE TABLE IF NOT EXISTS ProductIngredient(
	ProductIngredientID int SERIAL PRIMARY KEY NOT NULL,
	ProductID int NOT NULL,
	IngredientID int NOT NULL,
""",
"""CREATE TABLE IF NOT EXISTS ProductMenu(
	ProductMenuID int SERIAL PRIMARY KEY NOT NULL,
	FoodMenuID int NOT NULL,
	ProductID int NOT NULL,
""",
"""CREATE TABLE IF NOT EXISTS ProductSale(
	ProductSaleID int SERIAL PRIMARY KEY NOT NULL,
	ProductID int NOT NULL,
	SaleID int NOT NULL,
	Note nvarchar(max) NULL, 
""",
"""CREATE TABLE IF NOT EXISTS ProductType(
	ProductTypeID int NOT NULL,
	ProductTypeName nvarchar(50) NOT NULL, 
	PRIMARY KEY (ProductTypeID)
""",
"""CREATE TABLE IF NOT EXISTS Register(
	RegisterID int NOT NULL,
	RegisterTypeID int NOT NULL,
	IsActive bit NOT NULL, 
	PRIMARY KEY (RegisterID)
""",
"""CREATE TABLE IF NOT EXISTS RegisterType(
	RegisterTypeID int NOT NULL,
	RegisterTypeName nvarchar(50) NOT NULL, 
	PRIMARY KEY (RegisterTypeID)
""",
"""CREATE TABLE IF NOT EXISTS Role(
	RoleID int SERIAL PRIMARY KEY NOT NULL,
	RoleName nvarchar(50) NOT NULL, 
	CreatedOn datetime NOT NULL, 
	ModifiedOn datetime NULL, 
	CreatedBy int NOT NULL,
	ModifiedBy int NULL,
""",
"""CREATE TABLE IF NOT EXISTS RolePermission(
	RolePermissionID int SERIAL PRIMARY KEY NOT NULL,
	RoleID int NOT NULL,
	PermissionID int NOT NULL,
CONSTRAINT IX_RolePermission UNIQUE NONCLUSTERED 
(
	PermissionID,
	RoleID
))""",
"""CREATE TABLE IF NOT EXISTS Sale(
	SaleID int SERIAL PRIMARY KEY NOT NULL,
	EmployeeID int NULL,
	RegisterID int NOT NULL,
	SurveyID int NOT NULL,
	PaymentMethod nvarchar(50) NOT NULL, 
	CreatedOn datetime NOT NULL, 
	ModifiedOn datetime NULL, 
	IsDelivered bit NULL, 
	IsCancelled bit NULL, 
""",
"""CREATE TABLE IF NOT EXISTS System(
	ConfigId nvarchar(50) NOT NULL,
	ConfigValue nvarchar(50) NOT NULL, 
	ConfigValueType nvarchar(50) NOT NULL, 
	IsEditable bit NOT NULL, 
	CreatedOn datetime NOT NULL, 
	ModifiedOn datetime NULL, 
	ModifiedBy int NULL,
	PRIMARY KEY (ConfigId)
""",
"""CREATE TABLE IF NOT EXISTS Title(
	TitleID int SERIAL PRIMARY KEY NOT NULL,
	TitleName nvarchar(50) NOT NULL, 
	MonthlyPay decimal(18, 2) NOT NULL, 
	ModifiedOn datetime NULL, 
""",
"""CREATE TABLE IF NOT EXISTS Toy(
	ToyID int SERIAL PRIMARY KEY NOT NULL,
	ToyName nvarchar(50) NOT NULL, 
	Promotion nvarchar(max) NOT NULL, 
	CreatedOn datetime NOT NULL, 
"""
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

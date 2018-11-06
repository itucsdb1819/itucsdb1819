import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
"""CREATE TABLE IF NOT EXISTS CustomerSurvey(
	SurveyID serial PRIMARY KEY,
	SaleID integer NOT NULL,
	SurveyGUID text NOT NULL, 
	Score decimal NOT NULL, 
	CustomerAddition text NULL, 
	CreatedOn timestamp NOT NULL, 
	CompletedOn timestamp NULL, 
	IsSurveyCodeExpired bool NOT NULL
)""",
"""CREATE TABLE IF NOT EXISTS Employee(
	EmployeeID serial PRIMARY KEY,
	RoleID integer NOT NULL,
	Name varchar(50) NOT NULL, 
	Surname varchar(50) NOT NULL, 
	CreatedOn timestamp NOT NULL, 
	ModifiedOn timestamp NULL, 
	IsActive bool NOT NULL, 
	TitleID integer NOT NULL
)""",
"""CREATE TABLE IF NOT EXISTS Expense(
	ExpenseID serial PRIMARY KEY,
	Amount decimal NOT NULL, 
	Description varchar(50) NOT NULL, 
	CreatedOn timestamp NOT NULL, 
	ModifiedOn timestamp NULL, 
	IsPremium bool NOT NULL, 
	CreatedBy integer NOT NULL,
	ModifiedBy integer NULL
)""",
"""CREATE TABLE IF NOT EXISTS FoodMenu(
	FoodMenuID serial PRIMARY KEY,
	ToyID integer NULL,
	Discount decimal NOT NULL, 
	IsActive bool NOT NULL, 
	IsChildrenOnly bool NOT NULL, 
	CreatedOn timestamp NOT NULL, 
	ModifiedOn timestamp NULL
)""",
"""CREATE TABLE IF NOT EXISTS Ingredient(
	IngredientID integer PRIMARY KEY,
	IngredienTypeID integer NOT NULL,
	IngredientName varchar(50) NOT NULL
)""",
"""CREATE TABLE IF NOT EXISTS IngredientType(
	IngredienTypeID integer PRIMARY KEY,
	IngredientTypeName varchar(50) NOT NULL
)""",
"""CREATE TABLE IF NOT EXISTS Localization(
	PK serial PRIMARY KEY,
	ResourceId varchar(50) NOT NULL, 
	LocaleId varchar(4) NOT NULL, 
	ResourceSet varchar(50) NOT NULL, 
	Value varchar(50) NOT NULL
)""",
"""CREATE TABLE IF NOT EXISTS Menu(
	MenuItemID integer PRIMARY KEY,
	MasterMenuItemID integer NULL,
	PermissionID integer NOT NULL,
	MenuItemName varchar(50) NOT NULL, 
	MenuItemPath varchar(50) NOT NULL, 
	IconPath varchar(50) NOT NULL, 
	IsActive bool NOT NULL
	)""",
"""CREATE TABLE IF NOT EXISTS Permission(
	PermissionID integer PRIMARY KEY,
	PermissionCode varchar(50) NOT NULL,
	PermissionName varchar(50) NOT NULL
)""",
"""CREATE TABLE IF NOT EXISTS Product(
	ProductID serial PRIMARY KEY,
	ProductTypeID integer NOT NULL,
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
	ProductIngredientID serial PRIMARY KEY,
	ProductID integer NOT NULL,
	IngredientID integer NOT NULL
)""",
"""CREATE TABLE IF NOT EXISTS ProductMenu(
	ProductMenuID serial PRIMARY KEY,
	FoodMenuID integer NOT NULL,
	ProductID integer NOT NULL
)""",
"""CREATE TABLE IF NOT EXISTS ProductSale(
	ProductSaleID serial PRIMARY KEY,
	ProductID integer NOT NULL,
	SaleID integer NOT NULL,
	Note text NULL 
)""",
"""CREATE TABLE IF NOT EXISTS ProductType(
	ProductTypeID integer PRIMARY KEY,
	ProductTypeName varchar(50) NOT NULL
)""",
"""CREATE TABLE IF NOT EXISTS Register(
	RegisterID integer PRIMARY KEY,
	RegisterTypeID integer NOT NULL,
	IsActive bool NOT NULL
)""",
"""CREATE TABLE IF NOT EXISTS RegisterType(
	RegisterTypeID integer PRIMARY KEY,
	RegisterTypeName varchar(50) NOT NULL
)""",
"""CREATE TABLE IF NOT EXISTS Role(
	RoleID serial PRIMARY KEY,
	RoleName varchar(50) NOT NULL, 
	CreatedOn timestamp NOT NULL, 
	ModifiedOn timestamp NULL, 
	CreatedBy integer NOT NULL,
	ModifiedBy integer NULL
)""",
"""CREATE TABLE IF NOT EXISTS RolePermission(
	RolePermissionID serial PRIMARY KEY,
	RoleID integer NOT NULL,
	PermissionID integer NOT NULL
)""",
"""CREATE TABLE IF NOT EXISTS Sale(
	SaleID serial PRIMARY KEY,
	EmployeeID integer NULL,
	RegisterID integer NOT NULL,
	SurveyID integer NOT NULL,
	PaymentMethod varchar(50) NOT NULL, 
	CreatedOn timestamp NOT NULL, 
	ModifiedOn timestamp NULL, 
	IsDelivered bool NULL, 
	IsCancelled bool NULL 
)""",
"""CREATE TABLE IF NOT EXISTS System(
	ConfigId varchar(50) PRIMARY KEY,
	ConfigValue varchar(50) NOT NULL, 
	ConfigValueType varchar(50) NOT NULL, 
	IsEditable bool NOT NULL, 
	CreatedOn timestamp NOT NULL, 
	ModifiedOn timestamp NULL, 
	ModifiedBy integer NULL
)""",
"""CREATE TABLE IF NOT EXISTS Title(
	TitleID serial PRIMARY KEY,
	TitleName varchar(50) NOT NULL, 
	MonthlyPay decimal NOT NULL, 
	ModifiedOn timestamp NULL
)""",
"""CREATE TABLE IF NOT EXISTS Toy(
	ToyID serial PRIMARY KEY,
	ToyName varchar(50) NOT NULL, 
	Promotion text NOT NULL, 
	CreatedOn timestamp NOT NULL 
)""",
"""ALTER TABLE CustomerSurvey ADD CONSTRAINT FK_CustomerSurvey_Sale FOREIGN KEY (SurveyID) REFERENCES Sale (SurveyID);
	ALTER TABLE CustomerSurvey VALIDATE CONSTRAINT FK_CustomerSurvey_Sale;
""",
"""ALTER TABLE Employee ADD CONSTRAINT FK_Employee_Role FOREIGN KEY (RoleID) REFERENCES Role (RoleID);
	ALTER TABLE Employee VALIDATE CONSTRAINT FK_Employee_Role;
""",
"""ALTER TABLE Employee ADD CONSTRAINT FK_Employee_Title FOREIGN KEY (TitleID) REFERENCES Title (TitleID);
	ALTER TABLE Employee VALIDATE CONSTRAINT FK_Employee_Title;
""",
"""ALTER TABLE Expense ADD CONSTRAINT FK_Expense_Employee FOREIGN KEY (CreatedBy) REFERENCES Employee (EmployeeID);
	ALTER TABLE Expense VALIDATE CONSTRAINT FK_Expense_Employee;
""",
"""ALTER TABLE Expense ADD CONSTRAINT FK_Expense_Employee1 FOREIGN KEY (ModifiedBy) REFERENCES Employee (EmployeeID);
	ALTER TABLE Expense VALIDATE CONSTRAINT FK_Expense_Employee1;
""",
"""ALTER TABLE FoodMenu ADD CONSTRAINT FK_FoodMenu_Toy FOREIGN KEY (ToyID) REFERENCES Toy (ToyID);
	ALTER TABLE FoodMenu VALIDATE CONSTRAINT FK_FoodMenu_Toy;
""",
"""ALTER TABLE Ingredient ADD CONSTRAINT FK_Ingredient_IngredientType FOREIGN KEY (IngredienTypeID) REFERENCES IngredientType (IngredienTypeID);
	ALTER TABLE Ingredient VALIDATE CONSTRAINT FK_Ingredient_IngredientType;
""",
"""ALTER TABLE Menu ADD CONSTRAINT FK_Menu_Menu FOREIGN KEY (MasterMenuItemID) REFERENCES Menu (MenuItemID);
	ALTER TABLE Menu VALIDATE CONSTRAINT FK_Menu_Menu;
""",
"""ALTER TABLE Product ADD CONSTRAINT FK_Product_PoductType FOREIGN KEY (ProductTypeID) REFERENCES ProductType (ProductTypeID);
	ALTER TABLE Product VALIDATE CONSTRAINT FK_Product_PoductType;
""",
"""ALTER TABLE ProductIngredient ADD CONSTRAINT FK_ProductIngredient_Ingredient FOREIGN KEY (IngredientID) REFERENCES Ingredient (IngredientID);
	ALTER TABLE ProductIngredient VALIDATE CONSTRAINT FK_ProductIngredient_Ingredient;
""",
"""ALTER TABLE ProductIngredient ADD CONSTRAINT FK_ProductIngredient_Product FOREIGN KEY (ProductID) REFERENCES Product (ProductID);
	ALTER TABLE ProductIngredient VALIDATE CONSTRAINT FK_ProductIngredient_Product;
""",
"""ALTER TABLE ProductMenu ADD CONSTRAINT FK_ProductMenu_FoodMenu FOREIGN KEY (FoodMenuID) REFERENCES FoodMenu (FoodMenuID);
	ALTER TABLE ProductMenu VALIDATE CONSTRAINT FK_ProductMenu_FoodMenu;
""",
"""ALTER TABLE ProductMenu ADD CONSTRAINT FK_ProductMenu_Product FOREIGN KEY (ProductID) REFERENCES Product (ProductID);
	ALTER TABLE ProductMenu VALIDATE CONSTRAINT FK_ProductMenu_Product;
""",
"""ALTER TABLE ProductSale ADD CONSTRAINT FK_ProductSale_Product FOREIGN KEY (ProductID) REFERENCES Product (ProductID);
	ALTER TABLE ProductSale VALIDATE CONSTRAINT FK_ProductSale_Product;
""",
"""ALTER TABLE ProductSale ADD CONSTRAINT FK_ProductSale_Sale FOREIGN KEY (SaleID) REFERENCES Sale (SaleID);
	ALTER TABLE ProductSale VALIDATE CONSTRAINT FK_ProductSale_Sale;
""",
"""ALTER TABLE Register ADD CONSTRAINT FK_Register_RegisterType FOREIGN KEY (RegisterTypeID) REFERENCES RegisterType (RegisterTypeID);
	ALTER TABLE Register VALIDATE CONSTRAINT FK_Register_RegisterType;
""",
"""ALTER TABLE Role ADD CONSTRAINT FK_Role_Employee FOREIGN KEY (CreatedBy) REFERENCES Employee (EmployeeID);
	ALTER TABLE Role VALIDATE CONSTRAINT FK_Role_Employee;
""",
"""ALTER TABLE Role ADD CONSTRAINT FK_Role_Employee1 FOREIGN KEY (ModifiedBy) REFERENCES Employee (EmployeeID);
	ALTER TABLE Role VALIDATE CONSTRAINT FK_Role_Employee1;
""",
"""ALTER TABLE RolePermission ADD CONSTRAINT FK_RolePermission_Permission FOREIGN KEY (PermissionID) REFERENCES Permission (PermissionID);
	ALTER TABLE RolePermission VALIDATE CONSTRAINT FK_RolePermission_Permission;
""",
"""ALTER TABLE RolePermission ADD CONSTRAINT FK_RolePermission_Role FOREIGN KEY (RoleID) REFERENCES Role (RoleID);
	ALTER TABLE RolePermission VALIDATE CONSTRAINT FK_RolePermission_Role;
""",
"""ALTER TABLE Sale ADD CONSTRAINT FK_Sale_Employee FOREIGN KEY (EmployeeID) REFERENCES Employee (EmployeeID);
	ALTER TABLE Sale VALIDATE CONSTRAINT FK_Sale_Employee;
""",
"""ALTER TABLE Sale ADD CONSTRAINT FK_Sale_Register FOREIGN KEY (RegisterID) REFERENCES Register (RegisterID);
	ALTER TABLE Sale VALIDATE CONSTRAINT FK_Sale_Register;
""",
"""ALTER TABLE Sale ADD CONSTRAINT FK_Sale_CustomerSurvey FOREIGN KEY (SaleID) REFERENCES CustomerSurvey (SaleID);
	ALTER TABLE Sale VALIDATE CONSTRAINT FK_Sale_CustomerSurvey;
""",
"""ALTER TABLE System ADD CONSTRAINT FK_System_Employee FOREIGN KEY (ModifiedBy) REFERENCES Employee (EmployeeID);
	ALTER TABLE System VALIDATE CONSTRAINT FK_System_Employee;
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

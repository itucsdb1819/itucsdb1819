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
 CONSTRAINT PK_CustomerSurvey PRIMARY KEY 
(
	SurveyID ASC
))""",
    """CREATE TABLE IF NOT EXISTS Employee(
	EmployeeID int IDENTITY(1,1) NOT NULL,
	RoleID int NOT NULL,
	Name nvarchar(50) NOT NULL, 
	Surname nvarchar(50) NOT NULL, 
	CreatedOn datetime NOT NULL, 
	ModifiedOn datetime NULL, 
	IsActive bit NOT NULL, 
	TitleID int NOT NULL,
 CONSTRAINT PK_Employee PRIMARY KEY 
(
	EmployeeID ASC
))""",
"""CREATE TABLE IF NOT EXISTS Expense(
	ExpenseID int IDENTITY(1,1) NOT NULL,
	Amount decimal(18, 2) NOT NULL, 
	Description nvarchar(50) NOT NULL, 
	CreatedOn datetime NOT NULL, 
	ModifiedOn datetime NULL, 
	IsPremium bit NOT NULL, 
	CreatedBy int NOT NULL,
	ModifiedBy int NULL,
 CONSTRAINT PK_Expense PRIMARY KEY 
(
	ExpenseID ASC
))""",
"""CREATE TABLE IF NOT EXISTS FoodMenu(
	FoodMenuID int IDENTITY(1,1) NOT NULL,
	ToyID int NULL,
	Discount decimal(18, 2) NOT NULL, 
	IsActive bit NOT NULL, 
	IsChildrenOnly bit NOT NULL, 
	CreatedOn datetime NOT NULL, 
	ModifiedOn datetime NULL, 
 CONSTRAINT PK_FoodMenu PRIMARY KEY 
(
	FoodMenuID ASC
))""",
"""CREATE TABLE IF NOT EXISTS Ingredient(
	IngredientID int NOT NULL,
	IngredienTypeID int NOT NULL,
	IngredientName nvarchar(50) NOT NULL, 
 CONSTRAINT PK_Ingredient PRIMARY KEY 
(
	IngredientID ASC
))""",
"""CREATE TABLE IF NOT EXISTS IngredientType(
	IngredienTypeID int NOT NULL,
	IngredientTypeName nvarchar(50) NOT NULL, 
 CONSTRAINT PK_IngredientType PRIMARY KEY 
(
	IngredienTypeID ASC
))""",
"""CREATE TABLE IF NOT EXISTS Localization(
	PK int IDENTITY(1,1) NOT NULL,
	ResourceId nvarchar(50) NOT NULL, 
	LocaleId varchar(4) NOT NULL, 
	ResourceSet nvarchar(50) NOT NULL, 
	Value nvarchar(50) NOT NULL, 
 CONSTRAINT PK_Localization PRIMARY KEY 
(
	PK ASC
))""",
"""CREATE TABLE IF NOT EXISTS Menu(
	MenuItemID int NOT NULL,
	MasterMenuItemID int NULL,
	PermissionID int NOT NULL,
	MenuItemName nvarchar(50) NOT NULL, 
	MenuItemPath nvarchar(50) NOT NULL, 
	IconPath nvarchar(50) NOT NULL, 
	IsActive bit NOT NULL, 
 CONSTRAINT PK_Menu PRIMARY KEY 
(
	MenuItemID ASC
))""",
"""CREATE TABLE IF NOT EXISTS Permission(
	PermissionID int NOT NULL,
	PermissionCode nvarchar(50) NOT NULL,
	PermissionName nvarchar(50) NOT NULL, 
 CONSTRAINT PK_Permission PRIMARY KEY 
(
	PermissionID ASC
))""",
"""CREATE TABLE IF NOT EXISTS Product(
	ProductID int NOT NULL,
	ProductTypeID int NOT NULL,
	ProductName nvarchar(50) NOT NULL, 
	Price decimal(18, 2) NOT NULL, 
	Calorie decimal(18, 2) NOT NULL, 
	Protein decimal(18, 2) NOT NULL, 
	Carbohydrate decimal(18, 2) NOT NULL, 
	Fat decimal(18, 2) NOT NULL, 
	Glucose decimal(18, 2) NOT NULL, 
	IsVegetarian bit NOT NULL, 
 CONSTRAINT PK_Product PRIMARY KEY 
(
	ProductID ASC
))""",
"""CREATE TABLE IF NOT EXISTS ProductIngredient(
	ProductIngredientID int IDENTITY(1,1) NOT NULL,
	ProductID int NOT NULL,
	IngredientID int NOT NULL,
 CONSTRAINT PK_ProductIngredient PRIMARY KEY 
(
	ProductIngredientID ASC
))""",
"""CREATE TABLE IF NOT EXISTS ProductMenu(
	ProductMenuID int IDENTITY(1,1) NOT NULL,
	FoodMenuID int NOT NULL,
	ProductID int NOT NULL,
 CONSTRAINT PK_ProductMenu PRIMARY KEY 
(
	ProductMenuID ASC
))""",
"""CREATE TABLE IF NOT EXISTS ProductSale(
	ProductSaleID int IDENTITY(1,1) NOT NULL,
	ProductID int NOT NULL,
	SaleID int NOT NULL,
	Note nvarchar(max) NULL, 
 CONSTRAINT PK_ProductSale PRIMARY KEY 
(
	ProductSaleID ASC
))""",
"""CREATE TABLE IF NOT EXISTS ProductType(
	ProductTypeID int NOT NULL,
	ProductTypeName nvarchar(50) NOT NULL, 
 CONSTRAINT PK_PoductType PRIMARY KEY 
(
	ProductTypeID ASC
))""",
"""CREATE TABLE IF NOT EXISTS Register(
	RegisterID int NOT NULL,
	RegisterTypeID int NOT NULL,
	IsActive bit NOT NULL, 
 CONSTRAINT PK_Register PRIMARY KEY 
(
	RegisterID ASC
))""",
"""CREATE TABLE IF NOT EXISTS RegisterType(
	RegisterTypeID int NOT NULL,
	RegisterTypeName nvarchar(50) NOT NULL, 
 CONSTRAINT PK_RegisterType PRIMARY KEY 
(
	RegisterTypeID ASC
))""",
"""CREATE TABLE IF NOT EXISTS Role(
	RoleID int IDENTITY(1,1) NOT NULL,
	RoleName nvarchar(50) NOT NULL, 
	CreatedOn datetime NOT NULL, 
	ModifiedOn datetime NULL, 
	CreatedBy int NOT NULL,
	ModifiedBy int NULL,
 CONSTRAINT PK_Role PRIMARY KEY 
(
	RoleID ASC
))""",
"""CREATE TABLE IF NOT EXISTS RolePermission(
	RolePermissionID int IDENTITY(1,1) NOT NULL,
	RoleID int NOT NULL,
	PermissionID int NOT NULL,
 CONSTRAINT PK_RolePermission PRIMARY KEY 
(
	RolePermissionID ASC
),
 CONSTRAINT IX_RolePermission UNIQUE NONCLUSTERED 
(
	PermissionID ASC,
	RoleID ASC
))""",
"""CREATE TABLE IF NOT EXISTS Sale(
	SaleID int IDENTITY(1,1) NOT NULL,
	EmployeeID int NULL,
	RegisterID int NOT NULL,
	SurveyID int NOT NULL,
	PaymentMethod nvarchar(50) NOT NULL, 
	CreatedOn datetime NOT NULL, 
	ModifiedOn datetime NULL, 
	IsDelivered bit NULL, 
	IsCancelled bit NULL, 
 CONSTRAINT PK_Sale PRIMARY KEY 
(
	SaleID ASC
))""",
"""CREATE TABLE IF NOT EXISTS System(
	ConfigId nvarchar(50) NOT NULL,
	ConfigValue nvarchar(50) NOT NULL, 
	ConfigValueType nvarchar(50) NOT NULL, 
	IsEditable bit NOT NULL, 
	CreatedOn datetime NOT NULL, 
	ModifiedOn datetime NULL, 
	ModifiedBy int NULL,
 CONSTRAINT PK_System PRIMARY KEY 
(
	ConfigId ASC
))""",
"""CREATE TABLE IF NOT EXISTS Title(
	TitleID int IDENTITY(1,1) NOT NULL,
	TitleName nvarchar(50) NOT NULL, 
	MonthlyPay decimal(18, 2) NOT NULL, 
	ModifiedOn datetime NULL, 
 CONSTRAINT PK_Title PRIMARY KEY 
(
	TitleID ASC
))""",
"""CREATE TABLE IF NOT EXISTS Toy(
	ToyID int IDENTITY(1,1) NOT NULL,
	ToyName nvarchar(50) NOT NULL, 
	Promotion nvarchar(max) NOT NULL, 
	CreatedOn datetime NOT NULL, 
 CONSTRAINT PK_Toy PRIMARY KEY 
(
	ToyID ASC
))""",
"""ALTER TABLE CustomerSurvey  WITH CHECK ADD  CONSTRAINT FK_CustomerSurvey_Sale FOREIGN KEY(SurveyID)
REFERENCES Sale (SurveyID)
GO
ALTER TABLE CustomerSurvey CHECK CONSTRAINT FK_CustomerSurvey_Sale
GO
ALTER TABLE Employee  WITH CHECK ADD  CONSTRAINT FK_Employee_Role FOREIGN KEY(RoleID)
REFERENCES Role (RoleID)
GO
ALTER TABLE Employee CHECK CONSTRAINT FK_Employee_Role
GO
ALTER TABLE Employee  WITH CHECK ADD  CONSTRAINT FK_Employee_Title FOREIGN KEY(TitleID)
REFERENCES Title (TitleID)
GO
ALTER TABLE Employee CHECK CONSTRAINT FK_Employee_Title
GO
ALTER TABLE Expense  WITH CHECK ADD  CONSTRAINT FK_Expense_Employee FOREIGN KEY(CreatedBy)
REFERENCES Employee (EmployeeID)
GO
ALTER TABLE Expense CHECK CONSTRAINT FK_Expense_Employee
GO
ALTER TABLE Expense  WITH CHECK ADD  CONSTRAINT FK_Expense_Employee1 FOREIGN KEY(ModifiedBy)
REFERENCES Employee (EmployeeID)
GO
ALTER TABLE Expense CHECK CONSTRAINT FK_Expense_Employee1
GO
ALTER TABLE FoodMenu  WITH CHECK ADD  CONSTRAINT FK_FoodMenu_Toy FOREIGN KEY(ToyID)
REFERENCES Toy (ToyID)
GO
ALTER TABLE FoodMenu CHECK CONSTRAINT FK_FoodMenu_Toy
GO
ALTER TABLE Ingredient  WITH CHECK ADD  CONSTRAINT FK_Ingredient_IngredientType FOREIGN KEY(IngredienTypeID)
REFERENCES IngredientType (IngredienTypeID)
GO
ALTER TABLE Ingredient CHECK CONSTRAINT FK_Ingredient_IngredientType
GO
ALTER TABLE Menu  WITH CHECK ADD  CONSTRAINT FK_Menu_Menu FOREIGN KEY(MasterMenuItemID)
REFERENCES Menu (MenuItemID)
GO
ALTER TABLE Menu CHECK CONSTRAINT FK_Menu_Menu
GO
ALTER TABLE Product  WITH CHECK ADD  CONSTRAINT FK_Product_PoductType FOREIGN KEY(ProductTypeID)
REFERENCES ProductType (ProductTypeID)
GO
ALTER TABLE Product CHECK CONSTRAINT FK_Product_PoductType
GO
ALTER TABLE ProductIngredient  WITH CHECK ADD  CONSTRAINT FK_ProductIngredient_Ingredient FOREIGN KEY(IngredientID)
REFERENCES Ingredient (IngredientID)
GO
ALTER TABLE ProductIngredient CHECK CONSTRAINT FK_ProductIngredient_Ingredient
GO
ALTER TABLE ProductIngredient  WITH CHECK ADD  CONSTRAINT FK_ProductIngredient_Product FOREIGN KEY(ProductID)
REFERENCES Product (ProductID)
GO
ALTER TABLE ProductIngredient CHECK CONSTRAINT FK_ProductIngredient_Product
GO
ALTER TABLE ProductMenu  WITH CHECK ADD  CONSTRAINT FK_ProductMenu_FoodMenu FOREIGN KEY(FoodMenuID)
REFERENCES FoodMenu (FoodMenuID)
GO
ALTER TABLE ProductMenu CHECK CONSTRAINT FK_ProductMenu_FoodMenu
GO
ALTER TABLE ProductMenu  WITH CHECK ADD  CONSTRAINT FK_ProductMenu_Product FOREIGN KEY(ProductID)
REFERENCES Product (ProductID)
GO
ALTER TABLE ProductMenu CHECK CONSTRAINT FK_ProductMenu_Product
GO
ALTER TABLE ProductSale  WITH CHECK ADD  CONSTRAINT FK_ProductSale_Product FOREIGN KEY(ProductID)
REFERENCES Product (ProductID)
GO
ALTER TABLE ProductSale CHECK CONSTRAINT FK_ProductSale_Product
GO
ALTER TABLE ProductSale  WITH CHECK ADD  CONSTRAINT FK_ProductSale_Sale FOREIGN KEY(SaleID)
REFERENCES Sale (SaleID)
GO
ALTER TABLE ProductSale CHECK CONSTRAINT FK_ProductSale_Sale
GO
ALTER TABLE Register  WITH CHECK ADD  CONSTRAINT FK_Register_RegisterType FOREIGN KEY(RegisterTypeID)
REFERENCES RegisterType (RegisterTypeID)
GO
ALTER TABLE Register CHECK CONSTRAINT FK_Register_RegisterType
GO
ALTER TABLE Role  WITH CHECK ADD  CONSTRAINT FK_Role_Employee FOREIGN KEY(CreatedBy)
REFERENCES Employee (EmployeeID)
GO
ALTER TABLE Role CHECK CONSTRAINT FK_Role_Employee
GO
ALTER TABLE Role  WITH CHECK ADD  CONSTRAINT FK_Role_Employee1 FOREIGN KEY(ModifiedBy)
REFERENCES Employee (EmployeeID)
GO
ALTER TABLE Role CHECK CONSTRAINT FK_Role_Employee1
GO
ALTER TABLE RolePermission  WITH CHECK ADD  CONSTRAINT FK_RolePermission_Permission FOREIGN KEY(PermissionID)
REFERENCES Permission (PermissionID)
GO
ALTER TABLE RolePermission CHECK CONSTRAINT FK_RolePermission_Permission
GO
ALTER TABLE RolePermission  WITH CHECK ADD  CONSTRAINT FK_RolePermission_Role FOREIGN KEY(RoleID)
REFERENCES Role (RoleID)
GO
ALTER TABLE RolePermission CHECK CONSTRAINT FK_RolePermission_Role
GO
ALTER TABLE Sale  WITH CHECK ADD  CONSTRAINT FK_Sale_Employee FOREIGN KEY(EmployeeID)
REFERENCES Employee (EmployeeID)
GO
ALTER TABLE Sale CHECK CONSTRAINT FK_Sale_Employee
GO
ALTER TABLE Sale  WITH CHECK ADD  CONSTRAINT FK_Sale_Register FOREIGN KEY(RegisterID)
REFERENCES Register (RegisterID)
GO
ALTER TABLE Sale CHECK CONSTRAINT FK_Sale_Register
GO
ALTER TABLE Sale  WITH CHECK ADD  CONSTRAINT FK_Sale_CustomerSurvey FOREIGN KEY(SaleID)
REFERENCES CustomerSurvey (SaleID)
GO
ALTER TABLE Sale CHECK CONSTRAINT FK_Sale_CustomerSurvey
GO
ALTER TABLE System  WITH CHECK ADD  CONSTRAINT FK_System_Employee FOREIGN KEY(ModifiedBy)
REFERENCES Employee (EmployeeID)
GO
ALTER TABLE System CHECK CONSTRAINT FK_System_Employee
GO"""
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

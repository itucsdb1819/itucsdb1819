import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
    """CREATE TABLE IF NOT EXISTS [dbo].[CustomerSurvey](
	[SurveyID] [int] NOT NULL,
	[SaleID] [int] NOT NULL,
	[SurveyGUID] [nvarchar](max) NOT NULL, --NON-key
	[Score] [decimal](18, 2) NOT NULL, --NON-key
	[CustomerAddition] [nvarchar](max) NULL, --NON-key
	[CreatedOn] [datetime] NOT NULL, --NON-key
	[CompletedOn] [datetime] NULL, --NON-key
	[IsSurveyCodeExpired] [bit] NOT NULL, --NON-key
 CONSTRAINT [PK_CustomerSurvey] PRIMARY KEY CLUSTERED 
(
	[SurveyID] ASC
))""",
    """CREATE TABLE IF NOT EXISTS [dbo].[Employee](
	[EmployeeID] [int] IDENTITY(1,1) NOT NULL,
	[RoleID] [int] NOT NULL,
	[Name] [nvarchar](50) NOT NULL, --NON-key
	[Surname] [nvarchar](50) NOT NULL, --NON-key
	[CreatedOn] [datetime] NOT NULL, --NON-key
	[ModifiedOn] [datetime] NULL, --NON-key
	[IsActive] [bit] NOT NULL, --NON-key
	[TitleID] [int] NOT NULL,
 CONSTRAINT [PK_Employee] PRIMARY KEY CLUSTERED 
(
	[EmployeeID] ASC
))""",
"""CREATE TABLE IF NOT EXISTS [dbo].[Expense](
	[ExpenseID] [int] IDENTITY(1,1) NOT NULL,
	[Amount] [decimal](18, 2) NOT NULL, --NON-key
	[Description] [nvarchar](50) NOT NULL, --NON-key
	[CreatedOn] [datetime] NOT NULL, --NON-key
	[ModifiedOn] [datetime] NULL, --NON-key
	[IsPremium] [bit] NOT NULL, --NON-key
	[CreatedBy] [int] NOT NULL,
	[ModifiedBy] [int] NULL,
 CONSTRAINT [PK_Expense] PRIMARY KEY CLUSTERED 
(
	[ExpenseID] ASC
))""",
"""CREATE TABLE IF NOT EXISTS [dbo].[FoodMenu](
	[FoodMenuID] [int] IDENTITY(1,1) NOT NULL,
	[ToyID] [int] NULL,
	[Discount] [decimal](18, 2) NOT NULL, --NON-key
	[IsActive] [bit] NOT NULL, --NON-key
	[IsChildrenOnly] [bit] NOT NULL, --NON-key
	[CreatedOn] [datetime] NOT NULL, --NON-key
	[ModifiedOn] [datetime] NULL, --NON-key
 CONSTRAINT [PK_FoodMenu] PRIMARY KEY CLUSTERED 
(
	[FoodMenuID] ASC
))""",
"""CREATE TABLE IF NOT EXISTS [dbo].[Ingredient](
	[IngredientID] [int] NOT NULL,
	[IngredienTypeID] [int] NOT NULL,
	[IngredientName] [nvarchar](50) NOT NULL, --NON-key
 CONSTRAINT [PK_Ingredient] PRIMARY KEY CLUSTERED 
(
	[IngredientID] ASC
))""",
"""CREATE TABLE IF NOT EXISTS [dbo].[IngredientType](
	[IngredienTypeID] [int] NOT NULL,
	[IngredientTypeName] [nvarchar](50) NOT NULL, --NON-key
 CONSTRAINT [PK_IngredientType] PRIMARY KEY CLUSTERED 
(
	[IngredienTypeID] ASC
))""",
"""CREATE TABLE IF NOT EXISTS [dbo].[Localization](
	[PK] [int] IDENTITY(1,1) NOT NULL,
	[ResourceId] [nvarchar](50) NOT NULL, --NON-key
	[LocaleId] [varchar](4) NOT NULL, --NON-key
	[ResourceSet] [nvarchar](50) NOT NULL, --NON-key
	[Value] [nvarchar](50) NOT NULL, --NON-key
 CONSTRAINT [PK_Localization] PRIMARY KEY CLUSTERED 
(
	[PK] ASC
))""",
"""CREATE TABLE IF NOT EXISTS [dbo].[Menu](
	[MenuItemID] [int] NOT NULL,
	[MasterMenuItemID] [int] NULL,
	[PermissionID] [int] NOT NULL,
	[MenuItemName] [nvarchar](50) NOT NULL, --NON-key
	[MenuItemPath] [nvarchar](50) NOT NULL, --NON-key
	[IconPath] [nvarchar](50) NOT NULL, --NON-key
	[IsActive] [bit] NOT NULL, --NON-key
 CONSTRAINT [PK_Menu] PRIMARY KEY CLUSTERED 
(
	[MenuItemID] ASC
))""",
"""CREATE TABLE IF NOT EXISTS [dbo].[Permission](
	[PermissionID] [int] NOT NULL,
	[PermissionCode] [nvarchar](50) NOT NULL,
	[PermissionName] [nvarchar](50) NOT NULL, --NON-key
 CONSTRAINT [PK_Permission] PRIMARY KEY CLUSTERED 
(
	[PermissionID] ASC
))""",
"""CREATE TABLE IF NOT EXISTS [dbo].[Product](
	[ProductID] [int] NOT NULL,
	[ProductTypeID] [int] NOT NULL,
	[ProductName] [nvarchar](50) NOT NULL, --NON-key
	[Price] [decimal](18, 2) NOT NULL, --NON-key
	[Calorie] [decimal](18, 2) NOT NULL, --NON-key
	[Protein] [decimal](18, 2) NOT NULL, --NON-key
	[Carbohydrate] [decimal](18, 2) NOT NULL, --NON-key
	[Fat] [decimal](18, 2) NOT NULL, --NON-key
	[Glucose] [decimal](18, 2) NOT NULL, --NON-key
	[IsVegetarian] [bit] NOT NULL, --NON-key
 CONSTRAINT [PK_Product] PRIMARY KEY CLUSTERED 
(
	[ProductID] ASC
))""",
"""CREATE TABLE IF NOT EXISTS [dbo].[ProductIngredient](
	[ProductIngredientID] [int] IDENTITY(1,1) NOT NULL,
	[ProductID] [int] NOT NULL,
	[IngredientID] [int] NOT NULL,
 CONSTRAINT [PK_ProductIngredient] PRIMARY KEY CLUSTERED 
(
	[ProductIngredientID] ASC
))""",
"""CREATE TABLE IF NOT EXISTS [dbo].[ProductMenu](
	[ProductMenuID] [int] IDENTITY(1,1) NOT NULL,
	[FoodMenuID] [int] NOT NULL,
	[ProductID] [int] NOT NULL,
 CONSTRAINT [PK_ProductMenu] PRIMARY KEY CLUSTERED 
(
	[ProductMenuID] ASC
))""",
"""CREATE TABLE IF NOT EXISTS [dbo].[ProductSale](
	[ProductSaleID] [int] IDENTITY(1,1) NOT NULL,
	[ProductID] [int] NOT NULL,
	[SaleID] [int] NOT NULL,
	[Note] [nvarchar](max) NULL, --NON-key
 CONSTRAINT [PK_ProductSale] PRIMARY KEY CLUSTERED 
(
	[ProductSaleID] ASC
))""",
"""CREATE TABLE IF NOT EXISTS [dbo].[ProductType](
	[ProductTypeID] [int] NOT NULL,
	[ProductTypeName] [nvarchar](50) NOT NULL, --NON-key
 CONSTRAINT [PK_PoductType] PRIMARY KEY CLUSTERED 
(
	[ProductTypeID] ASC
))""",
"""CREATE TABLE IF NOT EXISTS [dbo].[Register](
	[RegisterID] [int] NOT NULL,
	[RegisterTypeID] [int] NOT NULL,
	[IsActive] [bit] NOT NULL, --NON-key
 CONSTRAINT [PK_Register] PRIMARY KEY CLUSTERED 
(
	[RegisterID] ASC
))""",
"""CREATE TABLE IF NOT EXISTS [dbo].[RegisterType](
	[RegisterTypeID] [int] NOT NULL,
	[RegisterTypeName] [nvarchar](50) NOT NULL, --NON-key
 CONSTRAINT [PK_RegisterType] PRIMARY KEY CLUSTERED 
(
	[RegisterTypeID] ASC
))""",
"""CREATE TABLE IF NOT EXISTS [dbo].[Role](
	[RoleID] [int] IDENTITY(1,1) NOT NULL,
	[RoleName] [nvarchar](50) NOT NULL, --NON-key
	[CreatedOn] [datetime] NOT NULL, --NON-key
	[ModifiedOn] [datetime] NULL, --NON-key
	[CreatedBy] [int] NOT NULL,
	[ModifiedBy] [int] NULL,
 CONSTRAINT [PK_Role] PRIMARY KEY CLUSTERED 
(
	[RoleID] ASC
))""",
"""CREATE TABLE IF NOT EXISTS [dbo].[RolePermission](
	[RolePermissionID] [int] IDENTITY(1,1) NOT NULL,
	[RoleID] [int] NOT NULL,
	[PermissionID] [int] NOT NULL,
 CONSTRAINT [PK_RolePermission] PRIMARY KEY CLUSTERED 
(
	[RolePermissionID] ASC
),
 CONSTRAINT [IX_RolePermission] UNIQUE NONCLUSTERED 
(
	[PermissionID] ASC,
	[RoleID] ASC
))""",
"""CREATE TABLE IF NOT EXISTS [dbo].[Sale](
	[SaleID] [int] IDENTITY(1,1) NOT NULL,
	[EmployeeID] [int] NULL,
	[RegisterID] [int] NOT NULL,
	[SurveyID] [int] NOT NULL,
	[PaymentMethod] [nvarchar](50) NOT NULL, --NON-key
	[CreatedOn] [datetime] NOT NULL, --NON-key
	[ModifiedOn] [datetime] NULL, --NON-key
	[IsDelivered] [bit] NULL, --NON-key
	[IsCancelled] [bit] NULL, --NON-key
 CONSTRAINT [PK_Sale] PRIMARY KEY CLUSTERED 
(
	[SaleID] ASC
))""",
"""CREATE TABLE IF NOT EXISTS [dbo].[System](
	[ConfigId] [nvarchar](50) NOT NULL,
	[ConfigValue] [nvarchar](50) NOT NULL, --NON-key
	[ConfigValueType] [nvarchar](50) NOT NULL, --NON-key
	[IsEditable] [bit] NOT NULL, --NON-key
	[CreatedOn] [datetime] NOT NULL, --NON-key
	[ModifiedOn] [datetime] NULL, --NON-key
	[ModifiedBy] [int] NULL,
 CONSTRAINT [PK_System] PRIMARY KEY CLUSTERED 
(
	[ConfigId] ASC
))""",
"""CREATE TABLE IF NOT EXISTS [dbo].[Title](
	[TitleID] [int] IDENTITY(1,1) NOT NULL,
	[TitleName] [nvarchar](50) NOT NULL, --NON-key
	[MonthlyPay] [decimal](18, 2) NOT NULL, --NON-key
	[ModifiedOn] [datetime] NULL, --NON-key
 CONSTRAINT [PK_Title] PRIMARY KEY CLUSTERED 
(
	[TitleID] ASC
))""",
"""CREATE TABLE IF NOT EXISTS [dbo].[Toy](
	[ToyID] [int] IDENTITY(1,1) NOT NULL,
	[ToyName] [nvarchar](50) NOT NULL, --NON-key
	[Promotion] [nvarchar](max) NOT NULL, --NON-key
	[CreatedOn] [datetime] NOT NULL, --NON-key
 CONSTRAINT [PK_Toy] PRIMARY KEY CLUSTERED 
(
	[ToyID] ASC
))""",
"""ALTER TABLE [dbo].[CustomerSurvey]  WITH CHECK ADD  CONSTRAINT [FK_CustomerSurvey_Sale] FOREIGN KEY([SurveyID])
REFERENCES [dbo].[Sale] ([SurveyID])
GO
ALTER TABLE [dbo].[CustomerSurvey] CHECK CONSTRAINT [FK_CustomerSurvey_Sale]
GO
ALTER TABLE [dbo].[Employee]  WITH CHECK ADD  CONSTRAINT [FK_Employee_Role] FOREIGN KEY([RoleID])
REFERENCES [dbo].[Role] ([RoleID])
GO
ALTER TABLE [dbo].[Employee] CHECK CONSTRAINT [FK_Employee_Role]
GO
ALTER TABLE [dbo].[Employee]  WITH CHECK ADD  CONSTRAINT [FK_Employee_Title] FOREIGN KEY([TitleID])
REFERENCES [dbo].[Title] ([TitleID])
GO
ALTER TABLE [dbo].[Employee] CHECK CONSTRAINT [FK_Employee_Title]
GO
ALTER TABLE [dbo].[Expense]  WITH CHECK ADD  CONSTRAINT [FK_Expense_Employee] FOREIGN KEY([CreatedBy])
REFERENCES [dbo].[Employee] ([EmployeeID])
GO
ALTER TABLE [dbo].[Expense] CHECK CONSTRAINT [FK_Expense_Employee]
GO
ALTER TABLE [dbo].[Expense]  WITH CHECK ADD  CONSTRAINT [FK_Expense_Employee1] FOREIGN KEY([ModifiedBy])
REFERENCES [dbo].[Employee] ([EmployeeID])
GO
ALTER TABLE [dbo].[Expense] CHECK CONSTRAINT [FK_Expense_Employee1]
GO
ALTER TABLE [dbo].[FoodMenu]  WITH CHECK ADD  CONSTRAINT [FK_FoodMenu_Toy] FOREIGN KEY([ToyID])
REFERENCES [dbo].[Toy] ([ToyID])
GO
ALTER TABLE [dbo].[FoodMenu] CHECK CONSTRAINT [FK_FoodMenu_Toy]
GO
ALTER TABLE [dbo].[Ingredient]  WITH CHECK ADD  CONSTRAINT [FK_Ingredient_IngredientType] FOREIGN KEY([IngredienTypeID])
REFERENCES [dbo].[IngredientType] ([IngredienTypeID])
GO
ALTER TABLE [dbo].[Ingredient] CHECK CONSTRAINT [FK_Ingredient_IngredientType]
GO
ALTER TABLE [dbo].[Menu]  WITH CHECK ADD  CONSTRAINT [FK_Menu_Menu] FOREIGN KEY([MasterMenuItemID])
REFERENCES [dbo].[Menu] ([MenuItemID])
GO
ALTER TABLE [dbo].[Menu] CHECK CONSTRAINT [FK_Menu_Menu]
GO
ALTER TABLE [dbo].[Product]  WITH CHECK ADD  CONSTRAINT [FK_Product_PoductType] FOREIGN KEY([ProductTypeID])
REFERENCES [dbo].[ProductType] ([ProductTypeID])
GO
ALTER TABLE [dbo].[Product] CHECK CONSTRAINT [FK_Product_PoductType]
GO
ALTER TABLE [dbo].[ProductIngredient]  WITH CHECK ADD  CONSTRAINT [FK_ProductIngredient_Ingredient] FOREIGN KEY([IngredientID])
REFERENCES [dbo].[Ingredient] ([IngredientID])
GO
ALTER TABLE [dbo].[ProductIngredient] CHECK CONSTRAINT [FK_ProductIngredient_Ingredient]
GO
ALTER TABLE [dbo].[ProductIngredient]  WITH CHECK ADD  CONSTRAINT [FK_ProductIngredient_Product] FOREIGN KEY([ProductID])
REFERENCES [dbo].[Product] ([ProductID])
GO
ALTER TABLE [dbo].[ProductIngredient] CHECK CONSTRAINT [FK_ProductIngredient_Product]
GO
ALTER TABLE [dbo].[ProductMenu]  WITH CHECK ADD  CONSTRAINT [FK_ProductMenu_FoodMenu] FOREIGN KEY([FoodMenuID])
REFERENCES [dbo].[FoodMenu] ([FoodMenuID])
GO
ALTER TABLE [dbo].[ProductMenu] CHECK CONSTRAINT [FK_ProductMenu_FoodMenu]
GO
ALTER TABLE [dbo].[ProductMenu]  WITH CHECK ADD  CONSTRAINT [FK_ProductMenu_Product] FOREIGN KEY([ProductID])
REFERENCES [dbo].[Product] ([ProductID])
GO
ALTER TABLE [dbo].[ProductMenu] CHECK CONSTRAINT [FK_ProductMenu_Product]
GO
ALTER TABLE [dbo].[ProductSale]  WITH CHECK ADD  CONSTRAINT [FK_ProductSale_Product] FOREIGN KEY([ProductID])
REFERENCES [dbo].[Product] ([ProductID])
GO
ALTER TABLE [dbo].[ProductSale] CHECK CONSTRAINT [FK_ProductSale_Product]
GO
ALTER TABLE [dbo].[ProductSale]  WITH CHECK ADD  CONSTRAINT [FK_ProductSale_Sale] FOREIGN KEY([SaleID])
REFERENCES [dbo].[Sale] ([SaleID])
GO
ALTER TABLE [dbo].[ProductSale] CHECK CONSTRAINT [FK_ProductSale_Sale]
GO
ALTER TABLE [dbo].[Register]  WITH CHECK ADD  CONSTRAINT [FK_Register_RegisterType] FOREIGN KEY([RegisterTypeID])
REFERENCES [dbo].[RegisterType] ([RegisterTypeID])
GO
ALTER TABLE [dbo].[Register] CHECK CONSTRAINT [FK_Register_RegisterType]
GO
ALTER TABLE [dbo].[Role]  WITH CHECK ADD  CONSTRAINT [FK_Role_Employee] FOREIGN KEY([CreatedBy])
REFERENCES [dbo].[Employee] ([EmployeeID])
GO
ALTER TABLE [dbo].[Role] CHECK CONSTRAINT [FK_Role_Employee]
GO
ALTER TABLE [dbo].[Role]  WITH CHECK ADD  CONSTRAINT [FK_Role_Employee1] FOREIGN KEY([ModifiedBy])
REFERENCES [dbo].[Employee] ([EmployeeID])
GO
ALTER TABLE [dbo].[Role] CHECK CONSTRAINT [FK_Role_Employee1]
GO
ALTER TABLE [dbo].[RolePermission]  WITH CHECK ADD  CONSTRAINT [FK_RolePermission_Permission] FOREIGN KEY([PermissionID])
REFERENCES [dbo].[Permission] ([PermissionID])
GO
ALTER TABLE [dbo].[RolePermission] CHECK CONSTRAINT [FK_RolePermission_Permission]
GO
ALTER TABLE [dbo].[RolePermission]  WITH CHECK ADD  CONSTRAINT [FK_RolePermission_Role] FOREIGN KEY([RoleID])
REFERENCES [dbo].[Role] ([RoleID])
GO
ALTER TABLE [dbo].[RolePermission] CHECK CONSTRAINT [FK_RolePermission_Role]
GO
ALTER TABLE [dbo].[Sale]  WITH CHECK ADD  CONSTRAINT [FK_Sale_Employee] FOREIGN KEY([EmployeeID])
REFERENCES [dbo].[Employee] ([EmployeeID])
GO
ALTER TABLE [dbo].[Sale] CHECK CONSTRAINT [FK_Sale_Employee]
GO
ALTER TABLE [dbo].[Sale]  WITH CHECK ADD  CONSTRAINT [FK_Sale_Register] FOREIGN KEY([RegisterID])
REFERENCES [dbo].[Register] ([RegisterID])
GO
ALTER TABLE [dbo].[Sale] CHECK CONSTRAINT [FK_Sale_Register]
GO
ALTER TABLE [dbo].[Sale]  WITH CHECK ADD  CONSTRAINT [FK_Sale_CustomerSurvey] FOREIGN KEY([SaleID])
REFERENCES [dbo].[CustomerSurvey] ([SaleID])
GO
ALTER TABLE [dbo].[Sale] CHECK CONSTRAINT [FK_Sale_CustomerSurvey]
GO
ALTER TABLE [dbo].[System]  WITH CHECK ADD  CONSTRAINT [FK_System_Employee] FOREIGN KEY([ModifiedBy])
REFERENCES [dbo].[Employee] ([EmployeeID])
GO
ALTER TABLE [dbo].[System] CHECK CONSTRAINT [FK_System_Employee]
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

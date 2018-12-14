import os
import sys
import psycopg2 as dbapi2

INIT_STATEMENTS = [
	"DROP TABLE IF EXISTS Localization",
	"DROP TABLE IF EXISTS Menu",
	"DROP TABLE IF EXISTS System CASCADE",

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
	IsVegetarian bool NOT NULL,
	IsActive bool NULL
)""",
"""CREATE TABLE IF NOT EXISTS ProductMenu(
	ProductMenuID serial REFERENCES FoodMenu,
	FoodMenuID integer NOT NULL,
	ProductID integer NOT NULL REFERENCES Product,
	PRIMARY KEY (ProductMenuID)
)""",
"""CREATE TABLE IF NOT EXISTS RegisterType(
	RegisterTypeID integer PRIMARY KEY,
	RegisterTypeName varchar(50) NOT NULL
)""",
"""CREATE TABLE IF NOT EXISTS Register(
	RegisterID integer ,
	RegisterTypeID integer NOT NULL REFERENCES RegisterType,
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
	Page text NOT NULL,
	LogType text NOT NULL,
	Traceback text NOT NULL,
	CreatedOn timestamp NOT NULL
)""",
	"UPDATE Product SET IsActive = true"

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
		VALUES ('Menu.SalesCreate', 'Menu', 'tr', 'Satış Girişi')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Employee.Create', 'PageText', 'tr', 'Çalışan Ekle')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Employee.Create', 'PageTitles', 'tr', 'Çalışan Ekle')""",
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
		VALUES ('Button.View', 'Buttons', 'tr', 'Göster')""",
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
		VALUES ('System', 'PageTitles', 'tr', 'Sistem Ayarları')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('SalesReport', 'PageTitles', 'tr', 'Satış Raporu')""",
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
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Sales.Create', 'PageText', 'tr', 'Satış Girişi')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Sales.Create', 'PageTitles', 'tr', 'Satış Girişi')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Employee.Role', 'PageText', 'tr', 'Rol')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Employee.FullName', 'PageText', 'tr', 'Adı Soyadı')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Employee.CreatedOn', 'PageText', 'tr', 'Eklenme Tarihi')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Employee.ModifiedOn', 'PageText', 'tr', 'Düzenlenme Tarihi')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Employee.IsActive', 'PageText', 'tr', 'Çalışıyor Mu?')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Employee.Title', 'PageText', 'tr', 'Ünvan')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Sales.Report', 'PageText', 'tr', 'Satış Raporu')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Products', 'PageTitles', 'tr', 'Ürünler')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Products.ProductTypeName', 'PageText', 'tr', 'Ürün Türü')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Products.ProductName', 'PageText', 'tr', 'Ürün Adı')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Products.Price', 'PageText', 'tr', 'Fiyatı')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Products.Calorie', 'PageText', 'tr', 'Kalori')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Products.Fat', 'PageText', 'tr', 'Yağ')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Products.Glucose', 'PageText', 'tr', 'Şeker')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Products.IsVegetarian', 'PageText', 'tr', 'Vejeteryan Mı?')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Products.Discount', 'PageText', 'tr', '% İndirim')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Products.IsChildrenOnly', 'PageText', 'tr', 'Çocuk Menüsü Mü?')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Products.Carbonhydrate', 'PageText', 'tr', 'Karbonhidrat')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('ProductType.Single', 'PageText', 'tr', 'Tekli')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('ProductType.Drink', 'PageText', 'tr', 'İçecek')""",		
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Toy.ToyName', 'PageText', 'tr', 'Oyuncak İsmi')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Product.FrenchFriesMedium', 'PageText', 'tr', 'Orta Boy Patates Kızartması')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Product.Hamburger', 'PageText', 'tr', 'Hamburger')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Product.CocaCola250', 'PageText', 'tr', '250ml CocaCola')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Sales.Personnel', 'PageText', 'tr', 'Satış Sorumlusu')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Sales.RegisterTypeName', 'PageText', 'tr', 'Kasa Tipi')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Sales.PaymentMethod', 'PageText', 'tr', 'Ödeme Yöntemi')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Sales.CreatedOn', 'PageText', 'tr', 'Satış Tarihi')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Sales.ModifiedOn', 'PageText', 'tr', 'Düzenlenme Tarihi')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Sales.IsDelivered', 'PageText', 'tr', 'Teslim Edildi Mi?')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Sales.IsCancelled', 'PageText', 'tr', 'İptal Edildi Mi?')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('', 'PageText', 'tr', 'Yok')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Button.Delete', 'Buttons', 'tr', 'Sil')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Product.Create', 'PageText', 'tr', 'Yeni Ürün Ekle')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('ProductType.Dessert', 'PageText', 'tr', 'Tatlı')""",
		"""INSERT INTO Localization (ResourceId, ResourceSet, LocaleId, Value)
		VALUES ('Product.Create', 'PageText', 'tr', 'Yeni Ürün Ekle')"""
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
""",
"""INSERT INTO Menu (MenuItemID, MasterMenuItemID, PermissionID, MenuItemName, MenuItemPath, IconPath, IsActive, HasChildren)
	VALUES (10, 3, 6, 'Menu.SalesCreate', '/sales_create', '', true, false)
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
            cursor.execute(statement)

        for statement in MENU_INSERT_STATEMENTS:
            cursor.execute(statement)

        for statement in SYSTEM_INSERT_STATEMENTS:
            cursor.execute(statement)	       
        
        for statement in LOCALIZATION_INSERT_STATEMENTS:
            cursor.execute(statement)

        connection.commit()
        cursor.close()

if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stdout)
        sys.exit(1)
    initialize(url)

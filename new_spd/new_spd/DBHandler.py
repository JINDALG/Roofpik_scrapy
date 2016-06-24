import MySQLdb

class DBHandler:
	def __init__(self):
		self.db = MySQLdb.connect("localhost", "root", "123456", "99acres")
		self.cur = self.db.cursor()

		self.insert_values  = 'INSERT INTO Data (Price, PricePerUnit, SuperBuiltupArea, CarpetArea, address, Location,  Washroom, PostedBy, PostingDate, ProjectName, Bedrooms, URL, maintainance, city,is_price_fixed, Website) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
		
		#self.insert_val = "INSERT INTO gurgaonData ( Price, PricePerUnit, Availability, SuperBuiltupArea, BuiltupArea, CarpetArea, address, Location,  Washroom,  Description, PostedBy, PostingDate, ProjectName, Bedrooms, Views, Searched, URL, Question, PROPERTYCODE ,BookingAmount , Deposit, GatedCommunity , PowerBackup , BookingINFO, AdditionalRooms, PropertyInfo , maintainance, Furnishing) VALUES (%(Price)s, %(PricePerUnit)s, %(Availability)s, %(SuperBuiltupArea)s , %(BuiltupArea)s, %(CarpetArea)s, %(address)s, %(Location)s , %(Washroom)s,  %(Description)s , %(PostedBy)s , %(PostingDate)s, %(ProjectName)s, %(Bedrooms)s, %(Views)s, %(Searched)s, %(URL)s, %(Question)s, %(PROPERTYCODE)s ,%(BookingAmount)s , %(Deposit)s, %(GatedCommunity)s , %(PowerBackup)s , %(BookingINFO)s, %(AdditionalRooms)s, %(PropertyInfo)s , %(maintainance)s, %(Furnishing)s )"

	def __del__(self):
		self.cur.close()
		self.db.close()


	def insert_into_db(self, Price, PricePerUnit, SuperBuiltupArea, CarpetArea, address, Location,  Washroom, PostedBy, PostingDate, ProjectName, Bedrooms, URL, maintainance,city, is_price_fixed, Website):
		#info = (Price, PricePerUnit, Availability, SuperBuiltupArea, BuiltupArea, CarpetArea, address, Location, Washroom, Description, PostedBy, PostingDate, ProjectName, Bedrooms, Views, Searched, URL, PROPERTYCODE,BookingAmount, Deposit, GatedCommunity, PowerBackup, BookingINFO, AdditionalRooms, PropertyInfo, maintainance, Furnishing)	
		self.cur.execute(self.insert_values, (Price, PricePerUnit, SuperBuiltupArea, CarpetArea, address, Location,  Washroom, PostedBy, PostingDate, ProjectName, Bedrooms, URL, maintainance, city, is_price_fixed, Website))

		self.db.commit()


		#self.cur.execute(self.insert_val, item)
		# field = (item['Price'], 
		# 	item['PricePerUnit'], item['Availability'] , item['SuperBuiltupArea'], 
		# 	item['BuiltupArea'], item['CarpetArea'], item['address'], 
		# 	item['Location'],  item['Washroom'], item['Description'], 
		# 	item['PostedBy'], item['PostingDate'], item['ProjectName'], item['Bedrooms'], item['Views'], 
		# 	item['Searched'], item['URL'], item['Question'], 
		# 	item['PROPERTYCODE'], item['BookingAmount'] , item['Deposit'], item['GatedCommunity'] , 
		# 	item['PowerBackup'] , item['BookingINFO'], item['AdditionalRooms'], item['PropertyInfo'], 
		# 	item['maintainance'], item['Furnishing'])


#CREATE TABLE test_table (Price FLOAT, PricePerUnit VARCHAR(60), Availability VARCHAR(30), SuperBuiltupArea INTEGER, BuiltupArea INTEGER, CarpetArea INTEGER, address VARCHAR(200), Location VARCHAR(100),  Washroom TINYINT,  Description VARCHAR(350), PostedBy VARCHAR(30), PostingDate VARCHAR(25), ProjectName VARCHAR(40), Bedrooms TINYINT, Views INTEGER, Searched INTEGER, URL VARCHAR(50), Question VARCHAR(150), PROPERTYCODE VARCHAR(20), BookingAmount INTEGER, Deposit INTEGER, GatedCommunity VARCHAR(10), PowerBackup VARCHAR(20), BookingINFO VARCHAR(100), AdditionalRooms VARCHAR(60), PropertyInfo VARCHAR(60), maintainance INTEGER, Furnishing VARCHAR(20))

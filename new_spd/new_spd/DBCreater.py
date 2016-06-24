import MySQLdb

def create_db():
	#MySQLdb.connect("localhost", "root", "beta", "shreyas")
	cnx = MySQLdb.connect("localhost", "root", "123456", "99acres")
	cursor = cnx.cursor()

	cursor.execute("CREATE TABLE IF NOT EXISTS Data (Price FLOAT, PricePerUnit VARCHAR(600), SuperBuiltupArea FLOAT, CarpetArea FLOAT ,address VARCHAR(200), Location VARCHAR(500),  Washroom TINYINT, PostedBy VARCHAR(100), PostingDate DATE, ProjectName VARCHAR(400), Bedrooms INTEGER,  URL VARCHAR(2000), maintainance VARCHAR(50), City VARCHAR(50), is_price_fixed BOOLEAN, Website VARCHAR(20))")

	insert = 'INSERT INTO (Price, PricePerUnit, SuperBuiltupArea, CarpetArea, address, Location,  Washroom, PostedBy, PostingDate, ProjectName, Bedrooms, URL, maintainance, city, is_price_fixed, Website) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

	#data = ( 1.0, 'dff',  'dsdf', 1,  1 , 1, 'fdfd',  'fdfd', 3,  'dfdf',  'dsd', 'sdd', 'dfdf',  3,  3, 344, 'dfdf',  'dffd',  'dffd', 344,  34,  'df', 'dfdf',  'fddf', 'dffd','dffd', 34, 'df')

	#cursor.execute(insert , ( 1.0, 'dff',  'dsdf', 1,  1 , 1, 'fdfd',  'fdfd', 3,  'dfdf',  'dsd', 'sdd', 'dfdf',  3,  3, 344, 'dfdf',  'dffd', 344,  34,  'df', 'dfdf',  'fddf', 'dffd','dffd', 34, 'df'))
	cnx.commit()
	cursor.close()
	cnx.close()


if __name__ == "__main__":
	create_db()
#INSERT INTO alpha (Price, PricePerUnit, Availability, SuperBuiltupArea, BuiltupArea, CarpetArea, address, Location,  Washroom,  Description, PostedBy, PostingDate, ProjectName, Bedrooms, Views, Searched, URL, Question, PROPERTYCODE ,BookingAmount , Deposit, GatedCommunity , PowerBackup , BookingINFO, AdditionalRooms, PropertyInfo , maintainance, Furnishing) VALUES (1.0, 'dff',  'dsdf', 1,  1 , 1, 'fdfd',  'fdfd', 3,  'dfdf',  'dsd', 'sdd', 'dfdf',  3,  3, 344, 'dfdf',  'dffd',  'dffd', 344,  34,  'df', 'dfdf',  'fddf', 'dffd','dffd', 34, 'df')
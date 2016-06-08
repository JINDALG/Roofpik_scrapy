import MySQLdb

def create_db():
	#MySQLdb.connect("localhost", "root", "beta", "shreyas")
	cnx = MySQLdb.connect("localhost", "root", "123456", "99acres")
	cursor = cnx.cursor()

	cursor.execute("CREATE TABLE IF NOT EXISTS Data (Price FLOAT, PricePerUnit VARCHAR(600), Availability VARCHAR(300), SuperBuiltupArea INTEGER, BuiltupArea INTEGER, CarpetArea INTEGER, address VARCHAR(200), Location VARCHAR(500),  Washroom TINYINT,  Description VARCHAR(350), PostedBy VARCHAR(100), PostingDate VARCHAR(25), ProjectName VARCHAR(400), Bedrooms INTEGER, Views INTEGER, Searched INTEGER, URL VARCHAR(2000), PROPERTYCODE VARCHAR(50), BookingAmount INTEGER, Deposit INTEGER, GatedCommunity VARCHAR(100), PowerBackup VARCHAR(60), BookingINFO VARCHAR(200), AdditionalRooms VARCHAR(60), PropertyInfo VARCHAR(600), maintainance INTEGER, Furnishing VARCHAR(40), City VARCHAR(50))")

	cursor.execute('CREATE TABLE IF NOT EXISTS Questions (Question VARCHAR(500))')
	cursor.execute('CREATE TABLE IF NOT EXISTS Trends (area VARCHAR(100), two_bedroom VARCHAR(50), three_bedroom VARCHAR(50), four_bedroom VARCHAR(50))')

	insert = 'INSERT INTO (Price, PricePerUnit, Availability, SuperBuiltupArea, BuiltupArea, CarpetArea, address, Location,  Washroom,  Description, PostedBy, PostingDate, ProjectName, Bedrooms, Views, Searched, URL,  PROPERTYCODE ,BookingAmount , Deposit, GatedCommunity , PowerBackup , BookingINFO, AdditionalRooms, PropertyInfo , maintainance, Furnishing) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

	#data = ( 1.0, 'dff',  'dsdf', 1,  1 , 1, 'fdfd',  'fdfd', 3,  'dfdf',  'dsd', 'sdd', 'dfdf',  3,  3, 344, 'dfdf',  'dffd',  'dffd', 344,  34,  'df', 'dfdf',  'fddf', 'dffd','dffd', 34, 'df')

	#cursor.execute(insert , ( 1.0, 'dff',  'dsdf', 1,  1 , 1, 'fdfd',  'fdfd', 3,  'dfdf',  'dsd', 'sdd', 'dfdf',  3,  3, 344, 'dfdf',  'dffd', 344,  34,  'df', 'dfdf',  'fddf', 'dffd','dffd', 34, 'df'))
	cnx.commit()
	cursor.close()
	cnx.close()


if __name__ == "__main__":
	create_db()
#INSERT INTO alpha (Price, PricePerUnit, Availability, SuperBuiltupArea, BuiltupArea, CarpetArea, address, Location,  Washroom,  Description, PostedBy, PostingDate, ProjectName, Bedrooms, Views, Searched, URL, Question, PROPERTYCODE ,BookingAmount , Deposit, GatedCommunity , PowerBackup , BookingINFO, AdditionalRooms, PropertyInfo , maintainance, Furnishing) VALUES (1.0, 'dff',  'dsdf', 1,  1 , 1, 'fdfd',  'fdfd', 3,  'dfdf',  'dsd', 'sdd', 'dfdf',  3,  3, 344, 'dfdf',  'dffd',  'dffd', 344,  34,  'df', 'dfdf',  'fddf', 'dffd','dffd', 34, 'df')
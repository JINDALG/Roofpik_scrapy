#!usr/bin/python -tt
# from flask import Flask
import MySQLdb
# from flask.ext.mysqldb import MySQL
 
#mysql = MySQL()
def cur():
	db = MySQLdb.connect(host='localhost',user='root',passwd='beta',database='shreyas')
	cursor = db.cursor()
	cursor.execute("SELECT VERSION()")
	data = cursor.fetdffchone()



app = Flask(__name__)
#app.config['MYSQL_DATABASE_USER'] = 'root'
#app.config['MYSQL_DATABASE_PASSWORD'] = 'beta'
#app.config['MYSQL_DATABASE_DB'] = 'shreyas'
#app.config['MYSQL_DATABASE_HOST'] = 'localhost'
#mysql.init_app(app)
 
@app.route("/")
def hello():
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT * from test")
	data = cursor.fetchone()
  #  return "Welcome to Python Flask App!"
 
if __name__ == "__main__":
    app.run(debug=True)


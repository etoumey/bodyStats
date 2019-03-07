import sqlite3


def createConnection():
	connection = sqlite3.connect('userData.db')
	return connection

def createTable(connection):
	sqlCreateTable = """ CREATE TABLE IF NOT EXISTS userData ( id integer PRIMARY KEY, date text NOT NULL, RHR text, SLEEP text, STRESS text ); """
	cursor = connection.cursor()
	cursor.execute(sqlCreateTable)

def writeData(connection):
	sql = ''' INSERT INTO userData(date, RHR, SLEEP, STRESS) VALUES(?,?,?,?)'''
	cursor = connection.cursor()
	cursor.execute(sql,('hi', 10, 20, 30))
	return cursor.lastrowid



connection = createConnection()
createTable(connection)
writeData(connection)
connection.close()
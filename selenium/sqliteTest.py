import sqlite3


def createConnection():
	connection = sqlite3.connect('userData.db')
	return connection

def createTable(connection):
	sqlCreateTable = """ CREATE TABLE IF NOT EXISTS userData (date text NOT NULL, RHR real, SLEEP real, STRESS real, ATL real, CTL real, PRIMARY KEY (date) ); """
	cursor = connection.cursor()
	cursor.execute(sqlCreateTable)

def writeData(connection):
	#sql = ''' INSERT INTO userData(date, RHR, SLEEP, STRESS, ATL, CTL) VALUES(?,?,?,?,?,?)'''
	cursor = connection.cursor()
	cursor.execute("INSERT INTO userData VALUES ('2019-06-08', 48, 20, 30, 10, 10)")
	connection.commit()
	return cursor.lastrowid



connection = createConnection()
createTable(connection)
writeData(connection)
connection.close()
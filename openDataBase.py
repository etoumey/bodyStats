import sqlite3


def openDataBase():

	connection = sqlite3.connect('userData.db')

	# Basic create if doesn't already exist logic 
	sqlCreateTableUserData = """ CREATE TABLE IF NOT EXISTS userData (date text NOT NULL, RHR real, SLEEP real, STRESS real, ATL real, CTL real, TSS, real, PRIMARY KEY (date) ); """
	sqlCreateTableActivities = """ CREATE TABLE IF NOT EXISTS activities (date text NOT NULL, FILEPATH real, DIST real, ELEV real, ELAPSEDTIME real, PRIMARY KEY (date) ); """

	cursor = connection.cursor()
	cursor.execute(sqlCreateTableUserData)
	cursor.execute(sqlCreateTableActivities)

	return connection
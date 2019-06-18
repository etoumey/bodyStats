import csv
import sqlite3
from os import listdir
import re
from datetime import datetime, timedelta
from matplotlib.patches import Rectangle


def initializeUserData():
	connection = sqlite3.connect('userData.db')
	sqlCreateTable = """ CREATE TABLE IF NOT EXISTS userData (date text NOT NULL, RHR real, SLEEP real, STRESS real, ATL real, CTL real, PRIMARY KEY (date) ); """
	cursor = connection.cursor()
	cursor.execute(sqlCreateTable)
	return connection


def getFileList():
	RHRFiles = []
	stressFiles = []
	sleepFiles = []

	allFiles = listdir('.')
	ii = 0
	for files in allFiles:
		if (re.search("RHR_\d{8}_\d{8}.csv", files)):
			RHRFiles.append(files)
		elif (re.search("SLEEP_\d{8}_\d{8}.csv", files)):
			sleepFiles.append(files)
		elif (re.search("STRESS_\d{8}_\d{8}.csv", files)):
			stressFiles.append(files)

	return RHRFiles, sleepFiles, stressFiles


def parseRHR(rhrFiles):
	dataRHR = []
	dateArray = []
	DOW = []

	for files in rhrFiles:
		ii = 0
		with open(files, 'r') as fh:
			tempRHR = csv.reader(fh)
			for rows in tempRHR:
				if (ii > 1 and ii <= 8):
					dataRHR.append(float(rows[1]))
					DOW.append(rows[0])
				ii = ii + 1
		dateArray.extend(pullDates(files, DOW))
		del DOW[:]
	return dataRHR, dateArray


def parseSleep(sleepFiles):
	dataSleep = []
	dateArray = []
	DOW = []

	for files in sleepFiles: 
		ii = 0
		with open(files, 'r') as fh:
			tempSleep = csv.reader(fh)
			for rows in tempSleep:
				if (ii > 1 and ii <= 8):
					hours, minutes = rows[2].split(":")
					minutes, garb = minutes.split(" ")
					dataSleep.append(float(hours) + float(minutes) / 60.0)
					DOW.append(rows[0])
				ii = ii + 1
		dateArray.extend(pullDates(files, DOW))
		del DOW[:]
	return dataSleep, dateArray


def parseStress(stressFiles):
	dataStress = []
	dateArray = []
	DOW = []

	for files in stressFiles:
		ii = 0
		with open(files, 'r') as fh:
			tempStress = csv.reader(fh)
			for rows in tempStress:
				if (ii > 1 and ii <= 8):
					dataStress.append(float(rows[1]))
					DOW.append(rows[0])
				ii = ii + 1
		dateArray.extend(pullDates(files, DOW))
		del DOW[:]
	return dataStress, dateArray


def pullDates(files, DOW):
	dateString = '%Y%m%d'
	tempSplit = re.split('_|\.', files)
	dateArray = []
	ii = 0
	offset = 0

	startDate = datetime.strptime(tempSplit[1], dateString)
	testDate = startDate
	#Convert from the date string in the data file to integer date numbers
	for days in DOW:
		if (DOW[ii] == 'Mon'):
			today = 0
		elif (DOW[ii] == 'Tue'):
			today = 1
		elif (DOW[ii] == 'Wed'):
			today = 2
		elif (DOW[ii] == 'Thu'):
			today = 3
		elif (DOW[ii] == 'Fri'):
			today = 4
		elif (DOW[ii] == 'Sat'):
			today = 5
		elif (DOW[ii] == 'Sun'):
			today = 6
		

		while (today != testDate.weekday()):
			offset = offset + 1 
			testDate = startDate + timedelta(days=offset)

		dateArray.append(testDate)
		ii = ii + 1
			
	return dateArray


def buildDB(connection, dates, data, column):
	cursor = connection.cursor()

	for ii in range(0,len(dates)):
		sql = '''SELECT date FROM userData WHERE date = ?''' 
		cursor.execute(sql, (dates[ii],))
		if cursor.fetchone():
			sql = '''UPDATE userData SET %s = ? WHERE date = ?''' % column
			cursor.execute(sql, (data[ii], dates[ii]))
		else:
			sql = '''INSERT INTO userData(date, %s) VALUES(?, ?)''' % column
			cursor.execute(sql, (dates[ii], data[ii]))
	#sql = '''SELECT * FROM userData ORDER BY date ASC;'''
	#cursor.execute(sql)
	connection.commit()





connection = initializeUserData()
rhrFiles, sleepFiles, stressFiles = getFileList()
dataRHR, datesRHR = parseRHR(rhrFiles)
print len(dataRHR) , len(datesRHR)
dataSleep, datesSleep = parseSleep(sleepFiles)
dataStress, datesStress = parseStress(stressFiles)
buildDB(connection, datesRHR, dataRHR, 'RHR')
buildDB(connection, datesSleep, dataSleep, 'SLEEP')
buildDB(connection, datesStress, dataStress, 'STRESS')

connection.close()
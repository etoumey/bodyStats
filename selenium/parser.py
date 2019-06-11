import json
import csv
import sqlite3
from os import listdir
import re
from datetime import datetime, timedelta


def initializeUserData():
	print "Initializing database..."
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
	dataRHR = [0,0,0,0,0,0,0]
	DOW = ['', '', '', '', '', '', '']
	ii = 0

	for files in rhrFiles:
		with open(files, 'r') as fh:
			tempRHR = csv.reader(fh)
			for rows in tempRHR:
				if (ii > 1 and ii <= 8):
					dataRHR[ii-2] = float(rows[1])
					DOW[ii-2] = rows[0]
				ii = ii + 1
			
		dateArray = pullDates(files, DOW)	
	return dataRHR, dateArray


def parseSleep(sleepFiles):
	dataSleep = [0,0,0,0,0,0]
	DOW = ['', '', '', '', '', '', '']
	ii = 0

	for files in sleepFiles: 
		with open(sleepFiles[0], 'r') as fh:
			tempSleep = csv.reader(fh)
			for rows in tempSleep:
				if (ii > 1 and ii <= 7):
					hours, minutes = rows[2].split(":")
					minutes, garb = minutes.split(" ")
					dataSleep[ii-2] = float(hours) + float(minutes) / 60.0
					DOW[ii-2] = rows[0]
				ii = ii + 1

		dateArray = pullDates(files, DOW)	
		print "Sleep parsed"
	return dataSleep, dateArray


def parseStress(stressFiles):
	dataStress = [0,0,0,0,0,0]
	DOW = ['', '', '', '', '', '', '']
	ii = 0

	for files in stressFiles:
		with open(stressFiles[0], 'r') as fh:
			tempStress = csv.reader(fh)
			for rows in tempStress:
				if (ii > 1 and ii <= 7):
					dataStress[ii-2] = float(rows[1])
					DOW[ii-2] = rows[0]
				ii = ii + 1

		dateArray = pullDates(files, DOW)	
		print "Stress parsed"
	return dataStress, dateArray


def pullDates(files, DOW):
	dateString = '%Y%m%d'
	tempSplit = re.split('_|\.', files)
	dateArray = []
	ii = 0
	offset = 0

	startDate = datetime.strptime(tempSplit[1], dateString)
	
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
		testDate = startDate + timedelta(days=offset)
		if (today == testDate.weekday()):
			dateArray.append(testDate)
			offset = offset + 1
			ii = ii + 1
		else:
			offset = offset + 1
	return dateArray


def buildDB(connection, datesRHR, dataRHR, dataSleep, dataStress):
	cursor = connection.cursor()
	
	for ii in range(0,len(datesRHR) - 1):
		cursor.execute('''REPLACE INTO userData(date, RHR, SLEEP, STRESS) VALUES(?, ?, ?, ?)''', (datesRHR[ii], dataRHR[ii], dataSleep[ii], dataStress[ii]))
	
	connection.commit()
	connection.close()




connection = initializeUserData()
rhrFiles, sleepFiles, stressFiles = getFileList()
dataRHR, datesRHR = parseRHR(rhrFiles)
dataSleep, datesSleep = parseSleep(sleepFiles)
dataStress, datesStress = parseStress(stressFiles)


buildDB(connection, datesRHR, dataRHR, dataSleep, dataStress)

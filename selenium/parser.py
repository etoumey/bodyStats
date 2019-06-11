import json
import csv
import sqlite3
from os import listdir
import re
from datetime import datetime


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

		print dataRHR
	return dataRHR


def parseSleep(sleepFiles):
	dataSleep = [0,0,0,0,0,0]
	ii = 0

	for files in sleepFiles: 
		startDate, endDate = pullDates(files)	
		with open(sleepFiles[0], 'r') as fh:
			tempSleep = csv.reader(fh)
			for rows in tempSleep:
				if (ii > 1 and ii <= 7):
					hours, minutes = rows[2].split(":")
					minutes, garb = minutes.split(" ")
					dataSleep[ii-2] = float(hours) + float(minutes) / 60.0
				ii = ii + 1
		print dataSleep
	return dataSleep


def parseStress(stressFiles):
	dataStress = [0,0,0,0,0,0]
	ii = 0

	for files in stressFiles:
		startDate, endDate = pullDates(files)
		with open(stressFiles[0], 'r') as fh:
			tempStress = csv.reader(fh)
			for rows in tempStress:
				if (ii > 1 and ii <= 7):
					dataStress[ii-2] = float(rows[1])
					ii = ii + 1
		print dataStress
	return dataStress


def pullDates(files, DOW):
	dateString = '%Y%m%d'
	tempSplit = re.split('_|\.', files)
	dateArray = []
	ii = 0

	startDate = datetime.strptime(tempSplit[1], dateString)

	for days in DOW:
		if (DOW[ii] == 'Mon'):
			DOW[ii] = 0
		elif (DOW[ii] == 'Tue'):
			DOW[ii] = 1
		elif (DOW[ii] == 'Wed'):
			DOW[ii] = 2
		elif (DOW[ii] == 'Thu'):
			DOW[ii] = 3
		elif (DOW[ii] == 'Fri'):
			DOW[ii] = 4
		elif (DOW[ii] == 'Sat'):
			DOW[ii] = 5
		elif (DOW[ii] == 'Sun'):
			DOW[ii] = 6	
		ii = ii + 1	

	print DOW

	
	#endDate = datetime.strptime(tempSplit[2], dateString)
	#for ii in DOW:




	#	startDate = (startDate + 1) % 7





connection = initializeUserData()
rhrFiles, sleepFiles, stressFiles = getFileList()
dataRHR = parseRHR(rhrFiles)
dataSleep = parseSleep(sleepFiles)
dataStress = parseStress(stressFiles)


#with open('userData', 'w+') as fh:#
#	json.dump(userData, fh)
#	fh.close()

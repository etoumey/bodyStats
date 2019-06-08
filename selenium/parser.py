import json
import csv


def initializeUserData():
	intiialize = '''
	{
		"day": "2019-06-08"
		[
			{
				"stress": "0",
				"sleep": "0",
				"rhr": "0",
				"atl": "0",
				"ctl": "0"
			}
		]
	}
	'''
	userData = json.loads(intiialize)
	print userData['day']
	return userData


def parseRHR():
	dataRHR = [0,0,0,0,0,0]
	ii = 0
	with open('WELLNESS_RESTING_HEART_RATE.csv', 'r') as fh:
		tempRHR = csv.reader(fh)
		for rows in tempRHR:
			if (ii > 1 and ii <= 7):
				dataRHR[ii-2] = float(rows[1])
			ii = ii + 1
	return dataRHR


def parseSleep():
	dataSleep = [0,0,0,0,0,0]
	ii = 0
	with open('SLEEP_SLEEP_DURATION.csv', 'r') as fh:
		tempSleep = csv.reader(fh)
		for rows in tempSleep:
			if (ii > 1 and ii <= 7):
				hours, minutes = rows[2].split(":")
				minutes, garb = minutes.split(" ")
				dataSleep[ii-2] = float(hours) + float(minutes) / 60.0
			ii = ii + 1
	return dataSleep




def parseStress():
	dataStress = [0,0,0,0,0,0]
	ii = 0
	with open('WELLNESS_AVERAGE_STRESS.csv', 'r') as fh:
		tempStress = csv.reader(fh)
		for rows in tempStress:
			if (ii > 1 and ii <= 7):
				dataStress[ii-2] = float(rows[1])
			ii = ii + 1
	return dataStress



try:
	with open('userData', 'r') as fh:
		userData = json.load(fh)
		fh.close()
		print "hi"
except:
	userData = initializeUserData()
print userData
dataRHR = parseRHR()
dataSleep = parseSleep()
dataStress = parseStress()
with open('userData', 'w+') as fh:
	json.dump(userData, fh)
	fh.close()

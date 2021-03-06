import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.dates import DateFormatter
from openDataBase import openDataBase
from scipy.stats import gaussian_kde
import json
from datetime import datetime, timedelta
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from haversine import haversine

from os import listdir, mkdir, path
from subprocess import call
import shutil
import sys
import re
import sqlite3


def parseFile(fileName):
	fh = open(fileName, 'r') #Open file with input name
	data = fh.readlines()
	fh.close
	# Initialize lists
	HR = [] 
	t = []
	lat = []
	lon = []
	elev = []
	for line in data: #Parse the date of the activity first
		if line.find("<time>") != -1:
			date = line[10:29]
			break

	secCheck = 0
	for line in data:  # Pass through all scanned data to get HR and time
		if line.find("<time>") != -1: # If a heart rate tag is found
			startT = line.find("<time>")
			stopT = line.find("</time>")
			if secCheck == 0: 
				t.append(float(line[startT+17:stopT-11])*3600+float(line[startT+20:stopT-8])*60+float(line[startT+23:stopT-5]))  #This line extracts the hours, minutes and seconds. They are all converted to seconds and appended to the time list
				secCheck = 1
			else:
				t[len(t)-1] = float(line[startT+17:stopT-11])*3600+float(line[startT+20:stopT-8])*60+float(line[startT+23:stopT-5])
				secCheck = 1
		elif line.find("<ns3:hr>") != -1:  
			if secCheck:
				startHR = line.find("<ns3:hr>") # Find start and end to split the line
				stopHR = line.find("</ns3:hr>")
				HR.append(float(line[startHR+8:stopHR])) # Extract only HR number. 8 is the length of the HR tag. <ns3:hr>
				secCheck = 0
		elif line.find("<trkpt") != -1:
			startLat = line.find("lat")
			startLon = line.find("lon")
			lat.append(float(line[startLat+5:startLon-2]))
			lon.append(float(line[startLon+5:-3]))
		elif line.find("<ele>") != -1:
			startElev = line.find("<ele>")
			endElev = line.find("</ele>")
			elev.append(float(line[startElev+5:endElev]))
	t[:] = [abs(i - t[0] + 86400) % 86400 for i in t]
	elapsedTime = t[-1] - t[0]
	dist = calcDist(lat, lon)
	elevGain = [max(0, elev[i+1] - elev[i]) for i in np.arange(len(elev) - 1)]
	totElevGain = np.sum(elevGain)*3.28084 #in feet
	#t.pop(0) #Delete first element of time which corresponds to activity start time. 
	return(HR, t, dist, elapsedTime, totElevGain, date)


def calcDist(lat, lon):
	if len(lat) != len(lon):
		raise ValueError("Latitude and Longitude arrays must have same length.")
	dist = 0.
	for i in np.arange(len(lat)-1):
		dist += haversine((lat[i+1], lon[i+1]), (lat[i], lon[i]), unit='mi') #Haversine formula for great circle distance
	return dist


def getZones():
	zones = [] # Initialize list
	fh = open('userData','r') # Read user data of format "RHR,MaxHR"
	data = fh.readlines()
	fh.close()
	HR = data[0].split(",")
	for i in range(0,6):  # Calculate each zone according to (Max HR - RHR) * [zone percentage] + RHR
		zones.append((float(HR[1]) - float(HR[0]))*((i+5.0)/10.0) + float(HR[0]))
	return(zones, (float(HR[1]) - float(HR[0])), float(HR[0]))


def getTimeInZones(HR, t, zones):
	tInZones = [0, 0, 0, 0, 0]  # Initialize at zero
	for i in range(0,len(HR)-1):
		if HR[i] < zones[0]:
			tInZones[0] += 1
		elif HR[i] < zones[2]:
			tInZones[1] += 1
		elif HR[i] < zones[3]:
			tInZones[2] += 1
		elif HR[i] < zones[4]:
			tInZones[3] += 1
		else:
			tInZones[4] += 1
	return tInZones


def calcTrimp(HR, t, HRR, RHR):
	trimp = 0
	for i in range(int(min(HR)), int(max(HR))):
		count = HR.count(i)
		Hr = ((i)- RHR) / HRR
		trimp += float(count) / 60.0 * Hr * .64 * np.exp(1.92 * Hr)
	return trimp


def addTrimpToDB(trimp, date, connection): # Need to add support for non existent PMC
	cursor = connection.cursor()

	#First add all days since your last activity 
	strDateFormat = "%Y-%m-%dT%H:%M:%S" #Just to extract the date from the string which includes the T, no T after this
	strDateFormatDB = "%Y-%m-%d 00:00:00"

	date = datetime.strptime(date, strDateFormat).strftime(strDateFormatDB)

	sql = '''SELECT date, IFNULL(TSS,0) FROM userData WHERE date = ?''' 
	cursor.execute(sql, (date,))
	row = cursor.fetchone()

	if row:
		dataBaseEntryTSS = trimp + float(row[1])
		sql = '''UPDATE userData SET TSS = ? WHERE date = ?''' 
		cursor.execute(sql, (dataBaseEntryTSS, date))
	else:
		sql = '''INSERT INTO userData(date, TSS) VALUES(?, ?)''' 
		cursor.execute(sql, (date, trimp))

	connection.commit()
	return


def addDataToDB(dist, elev, elapsedTime, trimp, date, connection): # Need to add support for non existent PMC
	cursor = connection.cursor()

	#First add all days since your last activity 
	strDateFormat = "%Y-%m-%dT%H:%M:%S" #Just to extract the date from the string which includes the T, no T after this
	#Activity EPOCH is what will be added as the primary key
	date = datetime.strptime(date, strDateFormat) 

	sql = '''SELECT date FROM activities WHERE date = ?''' 
	cursor.execute(sql, (date,))
	
	if cursor.fetchone():
		sql = '''UPDATE activities SET DIST = ? WHERE date = ?''' 
		cursor.execute(sql, (dist, date))
	else:
		sql = '''INSERT INTO activities(date, DIST) VALUES(?, ?)''' 
		cursor.execute(sql, (date, dist))
		
	sql = '''UPDATE activities SET ELEV = ? WHERE date = ?''' 
	cursor.execute(sql, (elev, date))
	sql = '''UPDATE activities SET ELAPSEDTIME = ? WHERE date = ?''' 
	cursor.execute(sql, (elapsedTime, date))
	sql = '''UPDATE activities SET TRIMP = ? WHERE date = ?''' 
	cursor.execute(sql, (trimp, date))

	connection.commit()
	return


def updatePMC(date, connection):
	cursor = connection.cursor()
	ATLDays = 7.0
	CTLDays = 42.0

	# We need to find the most recent non-null ATL/CTL entry in the DB
	sql = '''SELECT * FROM userData WHERE ATL IS NULL ORDER BY date ASC'''
	startDate = cursor.execute(sql).fetchone()

	if startDate:
		dateString = "%Y-%m-%d %H:%M:%S"
		dateStringT = "%Y-%m-%dT%H:%M:%S"
		startDate = datetime.strptime(startDate[0], dateString)
		endDate = datetime.strptime(date, dateStringT)
		delta = endDate - startDate

		sql = '''SELECT ATL, CTL, IFNULL(TSS, 0) FROM userData WHERE date = ?;'''
		sqlUpd = '''UPDATE userData SET ATL = ?, CTL = ? WHERE date = ?''' 
		sqlIns = '''INSERT INTO userData(date) VALUES(?)'''
		# to calculate today, we need to fetch yesterday first
		try:
			stats = cursor.execute(sql, (startDate + timedelta(days=-1),)).fetchone()
			ATLYesterday = stats[0]
			CTLYesterday = stats[1]
		except:
			ATLYesterday = 0
			CTLYesterday = 0

		for ii in range (0, delta.days + 1):
			currentDate = startDate + timedelta(days=ii)
			stats = cursor.execute(sql, (currentDate,)).fetchone()
			if stats:
				TSSToday = float(stats[2])
			else:
				cursor.execute(sqlIns, (currentDate,))
			ATLToday = ATLYesterday + (TSSToday - ATLYesterday) / ATLDays
			CTLToday = CTLYesterday + (TSSToday - CTLYesterday) / CTLDays
			ATLYesterday = ATLToday
			CTLYesterday = CTLToday
			cursor.execute(sqlUpd, (ATLToday, CTLToday, currentDate))

		connection.commit()
	else:
		pass


def generatePlot(HR, t, zones, tInZones):
	plt.rc('text', usetex=True)
	plt.rc('font', family='serif')
	plt.figure()
	plt.plot(t, HR)
	plt.grid()
	plt.xlabel(r'\textbf{Time} (s)')
	plt.ylabel(r'\textbf{HR} (bpm)')
	plt.title(r'\textbf{Heart Rate Over Time}')
	currentAxis = plt.gca()
	currentAxis.add_patch(Rectangle((0, (zones[4])), t[len(t)-1], zones[5] - zones[4], alpha=.2, label='Z5', facecolor='#cc0000'))
	currentAxis.add_patch(Rectangle((0, (zones[3])), t[len(t)-1], zones[4] - zones[3], alpha=.2, label='Z4', facecolor='#cc8400'))
	currentAxis.add_patch(Rectangle((0, (zones[2])), t[len(t)-1], zones[3] - zones[2], alpha=.2, label='Z3', facecolor='#1ecc00'))
	currentAxis.add_patch(Rectangle((0, (zones[1])), t[len(t)-1], zones[2] - zones[1], alpha=.2, label='Z2', facecolor='#6dc9ff'))
	currentAxis.add_patch(Rectangle((0, (zones[0])), t[len(t)-1], zones[1] - zones[0], alpha=.2, label='Z1', facecolor='#d142f4'))

	plt.legend(loc=4)
	plt.savefig('activityArchive/src/timeHistory.pdf')


	plt.figure()
	#z1, z2, z3, z4, z5 = plt.barh(np.arange(1,6),tInZones)
	labels = 'Z1', 'Z2', 'Z3', 'Z4', 'Z5'
	colors = ['#d142f4', '#6dc9ff', '#1ecc00', '#cc8400', '#cc0000']
	plt.pie(tInZones, labels = labels, explode = (.05,.05,.05,.05,.05), colors = colors)
	plt.title(r'\textbf{Time in Zones}')
	plt.savefig('activityArchive/src/pie.pdf')


	iqr = np.subtract(*np.percentile(HR, [75, 25])) # interquartile range
	nbins = int((max(HR)-min(HR))/(2.0*iqr/(len(HR)**(1.0/3.0)))) #Freedman-Diaconis rule for number of bins in histogram

	plt.figure()
	kde = gaussian_kde(HR)
	x = np.linspace(min(HR)-10, max(HR)+10, 500)
	pdf = kde.evaluate(x)
	currentAxis = plt.gca()
	currentAxis.add_patch(Rectangle(((zones[4]), 0), zones[5] - zones[4], max(pdf)*1.5, alpha=.2, label='Z5', facecolor='#cc0000'))
	currentAxis.add_patch(Rectangle(((zones[3]), 0), zones[4] - zones[3], max(pdf)*1.5, alpha=.2, label='Z4', facecolor='#cc8400'))
	currentAxis.add_patch(Rectangle(((zones[2]), 0), zones[3] - zones[2], max(pdf)*1.5, alpha=.2, label='Z3', facecolor='#1ecc00'))
	currentAxis.add_patch(Rectangle(((zones[1]), 0), zones[2] - zones[1], max(pdf)*1.5, alpha=.2, label='Z2', facecolor='#6dc9ff'))
	currentAxis.add_patch(Rectangle(((zones[0]), 0), zones[1] - zones[0], max(pdf)*1.5, alpha=.2, label='Z1', facecolor='#d142f4'))
	currentAxis.plot(x, pdf)
	plt.hist(HR,density=1, bins = nbins)
	plt.legend(loc=2)
	plt.title(r'\textbf{Heart Rate Histogram and PDF}')
	plt.ylim((0,max(pdf)*1.5))
	plt.savefig('activityArchive/src/hist.pdf')
	plt.close()


def printPMCMode():
	plt.rc('text', usetex=True)
	plt.rc('font', family='serif')

	with open('PMCData', 'r') as fh:
		PMC = json.load(fh)
		fh.close()

	dateFormat = "%Y-%m-%d %H:%M:%S"
	plotFormat = "%m/%d/%Y"
	dates = [l[0] for l in PMC]
	dates = [datetime.strptime(d, dateFormat) for d in dates]
	#dates = [datetime.strptime(d, dateFormat).strftime(plotFormat) for d in dates]
	ATL = [l[2] for l in PMC]
	CTL = [l[3] for l in PMC]
	
	endIndex = len(dates) 
	if endIndex > 60:
		startIndex = endIndex - 60
	else:
		startIndex = 0


	fig = plt.figure()
	axis = fig.add_subplot(1,1,1)
	axis.xaxis.set_major_formatter(DateFormatter('%m/%d'))
	plt.plot(dates[startIndex:endIndex], ATL[startIndex:endIndex])
	plt.plot(dates[startIndex:endIndex], CTL[startIndex:endIndex])
	plt.grid()
	plt.xlabel(r'\textbf{Time}')
	plt.ylabel(r'\textbf{Training Load}')
	plt.title(r'\textbf{Performance Manager Chart}')
	plt.show(block=False)
	plt.savefig('activityArchive/src/PMC.pdf')
	plt.close()


def getFileList(connection):
	gpxFiles = []

	allFiles = listdir('.')
	for files in allFiles:
		if re.search("[a-zA-Z0-9]*.gpx", files):
			gpxFiles.append(files)
	newFiles = []
	isNewFile = 0

	strDateFormat = "%Y-%m-%dT%H:%M:%S" #Just to extract the date from the string which includes the T, no T after this
	strDateFormatDB = "%Y-%m-%d %H:%M:%S" 

	for file in gpxFiles:
		fh = open(file, 'r') #Open file with input name
		data = fh.readlines()
		fh.close
		for line in data: #Parse the date of the activity and we'll check if it's in the PMC
			if line.find("<time>") != -1:
				date = line[10:29]
				date = datetime.strptime(date, strDateFormat).strftime(strDateFormatDB)

				sqlTest = '''SELECT date FROM activities WHERE date = ?''' 
				cursor = connection.cursor()

				cursor.execute(sqlTest, (date,))
				if cursor.fetchone():
					pass
				else:
					newFiles.append(file)
					isNewFile = 1
				break
	if isNewFile:
		print("New files found!")
	else:
		print("Nothing new found, plotting PMC")
	return newFiles


def makeReport(trimp, date):
	printPMCMode()
	reportFlag = 1 #Controls whether or not tex file gets compiled and archive is created. 
	archiveLocation = 'activityArchive/' + date
	if path.isdir(archiveLocation):
		shutil.rmtree(archiveLocation)
	
	mkdir(archiveLocation)
	shellCommand = 'pdflatex --output-directory ' + archiveLocation + ' --jobname=' + date + ' activityArchive/src/temp.tex' 
	call(shellCommand, shell=True)
	cleanUpCommand = 'rm ' + archiveLocation +'/*.log'
	call(cleanUpCommand, shell=True)
	cleanUpCommand = 'rm ' + archiveLocation +'/*.aux'
	call(cleanUpCommand, shell=True)


def getNotes(date, trimp, HR):
	noteContent = input('Please enter a workout note for ' + str(date) + ' with a TRIMP of ' + str(trimp) + ':')
	with open('activityArchive/src/notes.tex', 'w') as fh:
		fh.write(str(noteContent))

	with open('activityArchive/src/trimp', 'w') as fh:
		fh.write(str(trimp))

	with open('activityArchive/src/hr', 'w') as fh:
		fh.write(str(np.mean(HR)))

############################################### Main script #############




connection = openDataBase()
newFiles = getFileList(connection)

if newFiles:
	for fileName in newFiles:
		print(fileName)
		HR, t, dist, elapsedTime, elev, date = parseFile(fileName)
		zones, HRR, RHR = getZones()
		tInZones = getTimeInZones(HR, t, zones)
		trimp = calcTrimp(HR, t, HRR, RHR)
		getNotes(date, trimp, HR)
		addTrimpToDB(trimp, date, connection)
		addDataToDB(dist, elev, elapsedTime, trimp, date, connection)
		## insert propagation step here. 
		updatePMC(date, connection)
		generatePlot(HR, t, zones, tInZones)
		makeReport(trimp, date)

printPMCMode()
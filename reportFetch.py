from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from openDataBase import openDataBase
from os import getcwd,remove, listdir, rename
from datetime import date, datetime, timedelta
import time
import argparse
import getpass
import sqlite3

def queryCredentials():
	#This function loads credentials from the specified file. May be replaced with a user prompt not in development
	try:
		fid = open("credentials.pass", 'r')
		cred = fid.readlines()
		fid.close()

	except IOError:
		cred = []
		print("Credentials file 'credentials.pass' not found. Supply ")
		username = input("Username: ")
		password = getpass.getpass(prompt='Password: ')

		cred.append(username + '\n')
		cred.append(password + '\n')

	print("Credentials sucessfully loaded...")
	return cred


def downloadReport(browser):
	waitTime = 20 #Seconds to wait on landing page to load
	exportXpath = '//*[@id="pageContainer"]/div/div[1]/div[2]/div/button'
	dateXpath = '//*[@id="pageContainer"]/div/div[2]/div[2]/div[2]/div/span[2]'

	# Inside reports window, switch to default frame
	browser.switch_to.default_content()

	exportButton = WebDriverWait(browser, waitTime).until(
		EC.element_to_be_clickable((By.XPATH, exportXpath))
	)
	if exportButton:
		exportButton.click()

	dateElement = WebDriverWait(browser, waitTime).until(
	EC.presence_of_element_located((By.XPATH, dateXpath)))
	dateRange = str(dateElement.text)

	return dateRange


def downloadActivity(browser):
	waitTime = 20
	dateXpath = '//*[@id="pageContainer"]/div/div[2]/ul/li[1]/div[2]'
	activityXpath = '/html/body/div[1]/div[3]/div[2]/div[3]/div/div/div[2]/ul/li[1]/div[4]/div[1]/a'
	preloaderXpath = '//*[@id="pageContainer"]/div/div[2]/div[1]'
	gearXpath = '//*[@id="activityToolbarViewPlaceholder"]/div[2]/div[3]/button/i'
	downloadXpath = '//*[@id="btn-export-gpx"]/a'
	arrowXpath = '//*[@id="activityIntroViewPlaceholder"]/div[2]/button[1]/i'

	browser.get('https://connect.garmin.com/modern/activities?activityType=running') #Activity page

	#Wait for the annoying element to become presenttop

	#browser.switch_to.default_content()
	#WebDriverWait(browser, waitTime).until(
#		EC.presence_of_element_located((By.XPATH, preloaderXpath))
#		)
	#DESTROY THE ANNOYING ELEMENT
#	annoyingElement = browser.find_element_by_xpath(preloaderXpath)
#	browser.execute_script("arguments[0].style.visibility='hidden'", annoyingElement)

	#continue with life like a good boy
	element = WebDriverWait(browser, waitTime).until(
		EC.visibility_of_element_located((By.XPATH, activityXpath)))

	browser.find_element_by_xpath(activityXpath).click()

	for i in range(1,1):
		WebDriverWait(browser, waitTime).until(
			EC.element_to_be_clickable((By.XPATH, gearXpath))
			)
		browser.find_element_by_xpath(gearXpath).click()
		
		WebDriverWait(browser, waitTime).until(
			EC.element_to_be_clickable((By.XPATH, downloadXpath))
			)	

		browser.find_element_by_xpath(downloadXpath).click()
		print("Downloaded another")
		browser.find_element_by_xpath(arrowXpath).click()


def renameReport(dateRange, report):
	if report == 'RHR':
		OldFileName = 'Resting Heart Rate.csv'
		NewFileString = 'RHR_'
	elif report == 'SLEEP':
		OldFileName = 'Sleep Time.csv'
		NewFileString = 'SLEEP_'
	elif report == 'STRESS':
		OldFileName = 'Stress Level.csv'
		NewFileString = 'STRESS_'

	if dateRange:
		dateString = formatDateString(dateRange)
		NewFileName = NewFileString + dateString + '.csv'
		rename(OldFileName, NewFileName)

	return NewFileName


def formatDateString(dateRange):
	month = [0,0]

	dateRange = dateRange.replace(',','') #strip out commas
	dateRange = dateRange.split(' ')

	if dateRange[3] == '-':
		monthIndex = 4
	else:
		monthIndex = 3

	for ii in [0, monthIndex]:
		if (dateRange[ii] == 'Jan'):
			month[int(ii/3)] = 1
		elif (dateRange[ii] == 'Feb'):
			month[int(ii/3)] = 2
		elif (dateRange[ii] == 'Mar'):
			month[int(ii/3)] = 3
		elif (dateRange[ii] == 'Apr'):
			month[int(ii/3)] = 4
		elif (dateRange[ii] == 'May'):
			month[int(ii/3)] = 5
		elif (dateRange[ii] == 'Jun'):
			month[int(ii/3)] = 6
		elif (dateRange[ii] == 'Jul'):
			month[int(ii/3)] = 7
		elif (dateRange[ii] == 'Aug'):
			month[int(ii/3)] = 8
		elif (dateRange[ii] == 'Sep'):
			month[int(ii/3)] = 9
		elif (dateRange[ii] == 'Oct'):
			month[int(ii/3)] = 10
		elif (dateRange[ii] == 'Nov'):
			month[int(ii/3)] = 11
		elif (dateRange[ii] == 'Dec'):
			month[int(ii/3)] = 12

	if monthIndex == 3:
		dateString = str(int(float(dateRange[5])*10000 + month[0]*100 + float(dateRange[1]))) + '_' + str(int(float(dateRange[5])*10000 + month[1]*100 + float(dateRange[4])))
	else:
		dateString = str(int(float(dateRange[2])*10000 + month[0]*100 + float(dateRange[1]))) + '_' + str(int(float(dateRange[6])*10000 + month[1]*100 + float(dateRange[5])))

	return dateString


def browserInit(downloadDir):

	# Set Firefox preferences -- specifically to download *.csv files w/o raising a confirmation dialog box
	ffProfile = webdriver.FirefoxProfile()
	ffProfile.set_preference('browser.download.folderList', 2) # custom location
	ffProfile.set_preference('browser.download.manager.showWhenStarting', False)
	ffProfile.set_preference('browser.download.dir', downloadDir)
	ffProfile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv, application/gpx+xml')

	#Setup browser as headless
	opts = Options()
	opts.headless = True

	# Instantiate a Firefox browser object with the above-specified profile settings
	print("Browser preferences configured")
	browser = webdriver.Firefox(ffProfile, options = opts)
	print("Launching browser")

	return browser


def cleanUp(downloadDir):
	for file in listdir(downloadDir):
		if file.endswith(".csv"):
			remove(file)


def login(browser):
	credentials = queryCredentials()
	browser.get('https://connect.garmin.com/modern')

	#input field is within an iframe
	element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "gauth-widget-frame-gauth-widget")))
	frame = browser.find_element_by_id('gauth-widget-frame-gauth-widget')
	browser.switch_to.frame(frame)

	element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "username")))

	#populate username and password
	try:
		usernameField = browser.find_element_by_id("username")
		usernameField.send_keys(credentials[0])
		element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "password")))

		passwordField = browser.find_element_by_id("password")
		passwordField.send_keys(credentials[1])
		passwordField.submit()
	
		# Wait for login confirmation
		browser.switch_to.default_content()
		element = WebDriverWait(browser, 20).until(
			EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[3]/header/div[1]/div'))
		)
		print("Login Success")

	except:
		print("Login Failure")


def clickArrow(browser):
	# Only need arrow if you want to do multiple weeks at a time.
	arrowXpath = '//*[@id="pageContainer"]/div/div[2]/div[2]/div[2]/div/span[1]/button[1]'
	dateXpath = '//*[@id="pageContainer"]/div/div[2]/div[2]/div[2]/div/span[2]'
	waitTime = 20

	browser.switch_to.default_content()
	dateElement = WebDriverWait(browser, waitTime).until(
		EC.presence_of_element_located((By.XPATH, dateXpath)))
	#dateElement = browser.find_element_by_xpath(dateXpath)
	pageDateRange = str(dateElement.text)
	currentDateRange = pageDateRange

	browser.find_element_by_xpath(arrowXpath).click()

	while pageDateRange == currentDateRange:
		dateElement = WebDriverWait(browser, waitTime).until(
			EC.presence_of_element_located((By.XPATH, dateXpath)))
		currentDateRange = str(dateElement.text)


def setDownloadFlag(desiredDate, dateRange):
	dateString = formatDateString(dateRange)
	dateString = dateString.split('_')
	startDate = datetime.strptime(dateString[0], '%Y%m%d')

	if desiredDate >= startDate:
		downloadFlag = 0
	else:
		downloadFlag = 1

	return downloadFlag


def getDesiredDate(connection, reportType):
	cursor = connection.cursor()
	dateFormat = "%Y-%m-%d %H:%M:%S"
	# Find the oldest NULL value of the given report type
	sql = '''SELECT * FROM userData WHERE %s IS NOT NULL ORDER BY date DESC''' % reportType
	desiredDate = cursor.execute(sql).fetchone()
	
	# Take the day before the first non-null day
	if desiredDate:
		desiredDate = datetime.strptime(desiredDate[0], dateFormat)
		if ((datetime.now() - desiredDate).days < 1):
			# Make it a zero so we can just skip-a-dip the report
			desiredDate = 0
	else:
		# If you are here, there are ONLY NULL values. Maybe you just got a new garmin
		desiredDate = datetime.now()

	return desiredDate


def main():
	# Initialize everything
	connection = openDataBase()
	downloadFlag = 0

	desiredDateRHR = getDesiredDate(connection, 'RHR')
	desiredDateStress = getDesiredDate(connection, 'STRESS')
	desiredDateSleep = getDesiredDate(connection, 'SLEEP')

	if (desiredDateRHR or desiredDateStress or desiredDateSleep):
		downloadDir = getcwd()
		# Head to garmin connect login page
		browser = browserInit(downloadDir)
		login(browser)

	if desiredDateRHR:
		browser.get('https://connect.garmin.com/modern/report/60/wellness/last_seven_days') #RHR report
		downloadFlag = 1

	while downloadFlag:
		try:
			dateRangeRHR = downloadReport(browser)
			RHRReport = renameReport(dateRangeRHR, 'RHR')
			print("RHR Download Success! %s" % RHRReport)
			downloadFlag = setDownloadFlag(desiredDateRHR, dateRangeRHR)
			if downloadFlag:
				clickArrow(browser)
		except:
			print("Error fetching RHR Data...")
			clickArrow(browser)


	if desiredDateStress:
		browser.get('https://connect.garmin.com/modern/report/63/wellness/last_seven_days') #Stress report
		downloadFlag = 1

	while downloadFlag:
		try:
			dateRangeStress = downloadReport(browser)
			stressReport = renameReport(dateRangeStress, 'STRESS')
			print("Stress Download Success! %s" % stressReport)
			downloadFlag = setDownloadFlag(desiredDateStress, dateRangeStress)
			if downloadFlag:
				clickArrow(browser)
		except:
			print("Error Fetching Stress Data...")
			clickArrow(browser)

	

	if desiredDateSleep:
		browser.get('https://connect.garmin.com/modern/report/26/wellness/last_seven_days') #Sleep report
		downloadFlag = 1

	while downloadFlag:
		try:
			dateRangeSleep = downloadReport(browser)
			sleepReport = renameReport(dateRangeSleep, 'SLEEP')
			print("Sleep Download Success! %s" % sleepReport)
			downloadFlag = setDownloadFlag(desiredDateSleep, dateRangeSleep)
			if downloadFlag:
				clickArrow(browser)
		except:
			print("Error Fetching Sleep Data...")
			clickArrow(browser)

	if (desiredDateRHR or desiredDateStress or desiredDateSleep):
		downloadActivity(browser)
		browser.quit()




if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = 'Fetches Resting Heart Rate (RHR), stress, and sleep reports from garmin connect up to a specified date.')
	args = parser.parse_args()

	main()

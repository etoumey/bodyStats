from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from os import getcwd,remove, listdir, rename
from datetime import date
import time


def queryCredentials():
	#This function loads credentials from the specified file. May be replaced with a user prompt not in development
	fid = open("credentials.pass", 'r')
	cred = fid.readlines()
	fid.close()
	print("Credentials sucessfully loaded...")
	return cred


def downloadReport(browser):
	waitTime = 20 #Seconds to wait on landing page to load
	exportXpath = '//*[@id="pageContainer"]/div/div[1]/div[2]/div/button'
	dateXpath = '//*[@id="pageContainer"]/div/div[2]/div[2]/div[2]/div/span[2]' 
	# Inside reports window, switch to default frame
	browser.switch_to_default_content()
	# Wait for page to load
	element = WebDriverWait(browser, waitTime).until(
		EC.element_to_be_clickable((By.XPATH, exportXpath))
	)
	browser.find_element_by_xpath(exportXpath).click()


	dateElement = browser.find_element_by_xpath(dateXpath)
	dateRange = str(dateElement.text)

	# Only need arrow if you want to do multiple weeks at a time. 
	#arrowXpath = '//*[@id="pageContainer"]/div/div[2]/div[2]/div[2]/div/span[1]/button[1]'
	#browser.find_element_by_xpath(arrowXpath).click()

	return dateRange


def renameReport(dateRange, report):
	if report == 'RHR':
		OldFileName = 'WELLNESS_RESTING_HEART_RATE.csv'
		NewFileString = 'RHR_'
	elif report == 'SLEEP':
		OldFileName = 'SLEEP_SLEEP_DURATION.csv'
		NewFileString = 'SLEEP_'
	elif report == 'STRESS':
		OldFileName = 'WELLNESS_AVERAGE_STRESS.csv'
		NewFileString = 'STRESS_'

	if dateRange:
		DateString = formatDateString(dateRange)
		NewFileName = NewFileString + DateString + '.csv'
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
			month[int(ii/2)] = 1
		elif (dateRange[ii] == 'Feb'):
			month[int(ii/2)] = 2
		elif (dateRange[ii] == 'Mar'):
			month[int(ii/2)] = 3
		elif (dateRange[ii] == 'Apr'):
			month[int(ii/2)] = 4
		elif (dateRange[ii] == 'May'):
			month[int(ii/2)] = 5
		elif (dateRange[ii] == 'Jun'):
			month[int(ii/2)] = 6
		elif (dateRange[ii] == 'Jul'):
			month[int(ii/2)] = 7		
		elif (dateRange[ii] == 'Aug'):
			month[int(ii/2)] = 8
		elif (dateRange[ii] == 'Sep'):
			month[int(ii/2)] = 9
		elif (dateRange[ii] == 'Oct'):
			month[int(ii/2)] = 10
		elif (dateRange[ii] == 'Nov'):
			month[int(ii/2)] = 11
		elif (dateRange[ii] == 'Dec'):
			month[int(ii/2)] = 12
	
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
	ffProfile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')

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
	browser.get('https://connect.garmin.com/modern/')

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
		print("Login Success")
		browser.switch_to_default_content()
		element = WebDriverWait(browser, 20).until(
			EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[3]/header/div[1]/div'))
		)
	except:
		print("Login Failure")





def main():
	downloadDir = getcwd()
	
		#   Head to garmin connect login page
	browser = browserInit(downloadDir)

	login(browser)

	

	try:
		browser.get('https://connect.garmin.com/modern/report/60/wellness/last_seven_days') #RHR report
		dateRangeRHR = downloadReport(browser)
		RHRReport = renameReport(dateRangeRHR, 'RHR')
		print("RHR Download Success! %s") % RHRReport

	except:
		print("Error fetching RHR Data...")
	try:
		browser.get('https://connect.garmin.com/modern/report/63/wellness/last_seven_days') #Stress report
		dateRangeStress = downloadReport(browser)
		stressReport = renameReport(dateRangeStress, 'STRESS')
		print("Stress Download Success! %s") % stressReport
	except:
		print("Error Fetching Stress Data...")
	try:
		browser.get('https://connect.garmin.com/modern/report/26/wellness/last_seven_days') #Sleep report
		dateRangeSleep = downloadReport(browser)
		sleepReport = renameReport(dateRangeSleep, 'SLEEP')
		print("Sleep Download Success! %s") % stressReport
	except:
		print("Error Fetching Sleep Data...")


	browser.quit()


	

if __name__ == "__main__":
	main()

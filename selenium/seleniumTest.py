
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from os import getcwd,remove, listdir
from datetime import date
import time

def queryCredentials():
	#This function loads credentials from the specified file. May be replaced with a user prompt not in development
	fid = open("credentials.pass", 'r')
	cred = fid.readlines()
	fid.close()
	print "Credentials sucessfully loaded..."
	return cred

def downloadReport(browser):
	waitTime = 60 #Seconds to wait on landing page to load
	exportXpath = '//*[@id="pageContainer"]/div/div[1]/div[2]/div/button'

	# Inside reports window, switch to default frame
	browser.switch_to_default_content()
	# Wait for page to load
	element = WebDriverWait(browser, waitTime).until(
		EC.element_to_be_clickable((By.XPATH, exportXpath))
	)
	browser.find_element_by_xpath(exportXpath).click()
	# Only need arrow if you want to do multiple weeks at a time. 
	#arrowXpath = '//*[@id="pageContainer"]/div/div[2]/div[2]/div[2]/div/span[1]/button[1]'
	#browser.find_element_by_xpath(arrowXpath).click()

def reportMerge(downloadDir):
	today = str(date.today())
	today = today.split("-")
	day = today[2]
	month = today[1]
	year = today[0]

	
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
	print "Browser preferences configured"
	browser = webdriver.Firefox(ffProfile, options = opts)
	print "Launching browser"
	
	return browser

def cleanUp(downloadDir):
	for file in listdir(downloadDir):
		if file.endswith(".csv"):
			remove(file)




def main():
	downloadDir = getcwd()
	credentials = queryCredentials()
	#   Head to garmin connect login page
	browser = browserInit(downloadDir)

	browser.get('https://connect.garmin.com/modern/report/60/wellness/last_seven_days')

	#input field is within an iframe
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
		print "Login Success"
	except:
		print "Login Failure"


	try:
		downloadReport(browser)
		print "RHR Download Success!"
		browser.get('https://connect.garmin.com/modern/report/63/wellness/last_seven_days') #Stress report
		downloadReport(browser)
		print "Stress Download Success!"
		browser.get('https://connect.garmin.com/modern/report/26/wellness/last_seven_days') #Sleep report
		downloadReport(browser)
		print "Sleep Download Success!"
	except:
		print "Error fetching reports..."
		cleanUp(downloadDir)

	browser.quit()
	reportMerge(downloadDir)

	

if __name__ == "__main__":
	main()

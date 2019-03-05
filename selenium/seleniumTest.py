
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from os import getcwd
from datetime import date
import time

def queryCredentials():

	fid = open("credentials.pass", 'r')
	cred = fid.readlines()
	fid.close()
	print "Credentials sucessfully loaded..."
	return cred

def downloadReport(browser):
	# Inside reports window, switch to default frame
	browser.switch_to_default_content()
	# Wait for page to load
	time.sleep(5)
	element = WebDriverWait(browser, 10).until(
		EC.presence_of_element_located((By.ID, "pageContainer"))
	)

	exportXpath = '//*[@id="pageContainer"]/div/div[1]/div[2]/div/button'
	browser.find_element_by_xpath(exportXpath).click()
	arrowXpath = '//*[@id="pageContainer"]/div/div[2]/div[2]/div[2]/div/span[1]/button[1]'
	browser.find_element_by_xpath(arrowXpath).click()

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
	opts.headless = False

	# Instantiate a Firefox browser object with the above-specified profile settings
	print "Browser preferences configured"
	browser = webdriver.Firefox(ffProfile, options = opts)
	print "Launching browser"
	
	return browser




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


	requiredWeeks = 5
	for x in range(0,requiredWeeks):
		#try:
		downloadReport(browser)
		print "Week %d Success!" % (x + 1)
#		except:
#			print "Download Failed, try again later"
#			exit()

	browser.quit()
	reportMerge(downloadDir)

	

if __name__ == "__main__":
	main()

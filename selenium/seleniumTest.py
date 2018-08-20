
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from os import getcwd
from datetime import date

def queryCredentials():

    fid = open("credentials.pass", 'r')
    cred = fid.readlines()
    fid.close()

    return cred

def downloadReport(browser):
	# Inside reports window, switch to default frame
    browser.switch_to_default_content()
    # Wait for page to load
    element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "pageContainer"))
    )

    exportXpath = '//*[@id="pageContainer"]/div/div[1]/div[2]/div/button'
    browser.find_element_by_xpath(exportXpath).click()
    arrowXpath = '//*[@id="pageContainer"]/div/div[2]/div[2]/div[1]/div/span[1]/button[1]'
    browser.find_element_by_xpath(arrowXpath).click()

def reportMerge(downloadDir):
	today = str(date.today())
	today = today.split("-")
	day = today[2]
	month = today[1]
	year = today[0]

	






def main():

    credentials = queryCredentials()
    downloadDir = getcwd()
    # Set Firefox preferences -- specifically to download *.csv files w/o raising a confirmation dialog box
    ffProfile = webdriver.FirefoxProfile()
    ffProfile.set_preference('browser.download.folderList', 2) # custom location
    ffProfile.set_preference('browser.download.manager.showWhenStarting', False)
    ffProfile.set_preference('browser.download.dir', downloadDir)
    ffProfile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')

    #Setup browser as headless
    #opts = Options()
    #opts.set_headless()
    #assert opts.headless
    #browser = Firefox(options=opts)

    # Instantiate a Firefox browser object with the above-specified profile settings
    browser = webdriver.Firefox(ffProfile)

    #   Head to garmin connect login page
    browser.get('https://connect.garmin.com/modern/report/60/wellness/last_seven_days')

    #input field is within an iframe
    frame = browser.find_element_by_id('gauth-widget-frame-gauth-widget')
    browser.switch_to.frame(frame)

    element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "username")))

    #populate username and password
    usernameField = browser.find_element_by_id("username")
    usernameField.send_keys(credentials[0])
    element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "password")))

    passwordField = browser.find_element_by_id("password")
    passwordField.send_keys(credentials[1])
    passwordField.submit()

    requiredWeeks = 0
    for x in range(0,requiredWeeks):
        try:
        	downloadReport(browser)
        except:
        	print "Download Failed, try again later"
        	exit()

    browser.quit()
    reportMerge(downloadDir)

    

if __name__ == "__main__":
    main()

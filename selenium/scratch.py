
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

def queryCredentials():
    fid = open("credentials.pass", 'r')
    cred = fid.readlines()
    fid.close()

    return cred

def main():
    
    credentials = queryCredentials()

    ffProfile = webdriver.FirefoxProfile()
    ffProfile.set_preference('browser.download.folderList', 2) # custom location
    ffProfile.set_preference('browser.download.manager.showWhenStarting', False)
    ffProfile.set_preference('browser.download.dir', '/tmp')
    ffProfile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')

    browser = webdriver.Firefox(ffProfile)
    browser.get('https://connect.garmin.com/modern/report/60/wellness/last_seven_days')

    frame = browser.find_element_by_id('gauth-widget-frame-gauth-widget')
    browser.switch_to.frame(frame)

    usernameField = browser.find_element_by_id("username")
    passwordField = browser.find_element_by_id("password")

    usernameField.send_keys(credentials[0])

    passwordField.send_keys(credentials[1])
    passwordField.submit()

    browser.switch_to_default_content()
    # Wait for page to load
    element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "pageContainer"))
    )
    exportXpath = '//*[@id="pageContainer"]/div/div[1]/div[2]/div/button'
    browser.find_element_by_xpath(exportXpath).click()
    
if __name__ == "__main__":
    main()

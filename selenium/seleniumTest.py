from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time

#profile = webdriver.FirefoxProfile()
#profile.set_preference('browser.download.folderList', 2) # custom location
#profile.set_preference('browser.download.manager.showWhenStarting', False)
#profile.set_preference('browser.download.dir', '/tmp')
#profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')

#Setup browser as headless
opts = Options()
#opts.set_headless()
#assert opts.headless
browser = Firefox(options=opts)

#Head to garmin connect login page
browser.get('https://connect.garmin.com/modern/report/60/wellness/last_seven_days')
#input field is within an iframe

frame = browser.find_element_by_id('gauth-widget-frame-gauth-widget')
browser.switch_to.frame(frame)

element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "username")))

#populate username and password
usernameField = browser.find_element_by_id("username")
passwordField = browser.find_element_by_id("password")
FID = open("credentials.pass", "r")
credentials = FID.readlines()
FID.close()
usernameField.send_keys(credentials[0])
passwordField.send_keys(credentials[1])
passwordField.submit()


# Inside reports window, switch to default frame
browser.switch_to_default_content()
# Wait for page to load
element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "pageContainer"))
    )

# Health and Fitness Tab
#healthAndFitnessXpath = '//*[@id="accordion2"]/div[3]/div[1]/a'
#browser.find_element_by_xpath(healthAndFitnessXpath).click()

# RHR tab
#browser.find_element_by_id('60').click()
#browser.navigate().refresh()
# Export button
exportXpath = '//*[@id="pageContainer"]/div/div[1]/div[2]/div/button'
browser.find_element_by_xpath(exportXpath).click()


#browser.quit()

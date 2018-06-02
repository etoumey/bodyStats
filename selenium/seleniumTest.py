from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


#Setup browser as headless
opts = Options()
#opts.set_headless()
#assert opts.headless
browser = Firefox(options=opts)

#Head to garmin connect login page
browser.get('https://connect.garmin.com/modern/report')
#input field is within an iframe
frame = browser.find_element_by_id('gauth-widget-frame-gauth-widget')
browser.switch_to.frame(frame)

#populate username and password
usernameField = browser.find_element_by_id("username")
usernameField.send_keys('etoumey@gmail.com')
passwordField = browser.find_element_by_id("password")
passwordField.send_keys("passWORD")
passwordField.submit()

exportXpath = "/html/body/div[1]/div[3]/div/div[3]/div/div[1]/div[2]/div/button"

try:
    element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "button"))
    )
finally:
    browser.quit()

#browser.find_element_by_class_name("page-navigation-action js-export-btn").click()

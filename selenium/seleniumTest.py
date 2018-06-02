from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

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
passwordField.send_keys("PASSWORD")
passwordField.submit()



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
passwordField = browser.find_element_by_id("password")
FID = open("credentials.pass", "r")
credentials = FID.readlines()
FID.close()
usernameField.send_keys(credentials[0])
passwordField.send_keys(credentials[1])
passwordField.submit()

delay = 10 # seconds
button = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'notify-agent')))
print "Page is ready!"


fhBig = open('bigFile.csv', 'w')

for x in range(0,75):
  fhCurrent = open('WELLNESS_RESTING_HEART_RATE (%s).csv' % str(75-x), 'r')
  fhBig.write(fhCurrent.read())

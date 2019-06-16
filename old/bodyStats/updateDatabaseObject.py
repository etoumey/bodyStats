# Class Definitions

class GCData:
  dowData = []
  data = []

# rhr class
class Rhr(GCData):

#def parseRHR(dayRHR, rhr):
  def parseRHR(self):
    # open a sample file and ignore the first two lines (headers)
    f = open('rhr_29apr2017.csv', 'r')
    rhrData = f.readlines()[2:]

    # loop over the file lines and parse the data
    for line in rhrData:
      dayTemp, rhrTemp = line.split(",")

      dayRHR.append(dayTemp)
      rhr.append(rhrTemp.rstrip('\n'))

    f.close()

  def printInfo(self):
    print self.dowData

# sleep class
class Sleep(GCData):




rhrUpdate = rhr()
for i in range(0,5):
  rhrUpdate.dowData.append(i) 

print rhrUpdate.dowData
print '\n\n'

rhrUpdate.printInfo()






def parseSleep(daySlp, sleep):
  f = open('slp_09jul2017.csv', 'r')
  sleepData = f.readlines()[2:]

  for line in sleepData:
    # the sleep file has column 2: sleep as a float, column3: sleep as hr:min
    dayTemp, sleepFractionTemp, sleepClockTemp = line.split(",")

    daySlp.append(dayTemp)
    sleep.append(sleepFractionTemp.rstrip('\n'))

  f.close()

def parseStep(dayStp, steps):
  f = open('stp_09jul2017.csv', 'r')
  stepData = f.readlines()[2:]

  for line in stepData:
    # step file has column 2: actual steps, column 3: goal steps
    dayTemp, stepTemp, stepGoalTemp = line.split(",")

    dayStp.append(dayTemp)
    steps.append(stepTemp.rstrip('\n'))

  f.close()


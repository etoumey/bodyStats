#! /usr/bin/env/python
import parseCSV


#compare new data to database 
def compareNewData(dayRHR, rhr):
  db = open('database.csv', 'r+')
  rhrData = f.readlines()[2:]

  # loop over the file lines and parse the data
  for line in rhrData:
    dayTemp, rhrTemp = line.split(",")

    dayRHR.append(dayTemp)
    rhr.append(rhrTemp.rstrip('\n'))

  f.close()

 

# define the empty lists
dayRHR = []
daySlp = []
dayStp = []
rhr    = []
sleep  = []
steps  = []

# parse the data files from Garmin Connect
parseCSV.parseRHR(dayRHR, rhr)

parseCSV.parseSleep(daySlp, sleep)

parseCSV.parseStep(dayStp, steps)





# test print
print dayRHR, rhr

print daySlp, sleep

print dayStp, steps

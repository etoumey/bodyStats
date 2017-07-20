#! /usr/bin/env/python
import parseCSV

# local variable definition
databaseMatchFlag = 0

# define the empty lists
dayRHR = []
daySlp = []
dayStp = []
rhr    = []
sleep  = []
steps  = []

# empty lists for importing the database
dayDB = [] 
dowDB = []
rhrDB = []
slpDB = []

# parse the data files from Garmin Connect
parseCSV.parseRHR(dayRHR, rhr)

parseCSV.parseSleep(daySlp, sleep)

parseCSV.parseStep(dayStp, steps)

# test print
print dayRHR, rhr

print daySlp, sleep

print dayStp, steps

## UPDATE DATABASE

# load the database in reverse for comparison
# note, if the file is too big to store in memory, this will not work

DBFileHandle = open('../tex/database.csv','r')

# read from EOF
DBFileHandle.seek(0, 2)
EOFPointer = DBFileHandle.tell() # return location of EOF pointer
DBFileHandle.seek(max(EOFPointer-1024, 0), 0) # move pointer back 1K
DBEnd = DBFileHandle.readlines() # read to end
DBEnd = DBEnd[-7:] # only need last seven lines

# Parse the info as in parseCSV
for line in DBEnd:
  dayTemp, dowTemp, rhrTemp, sleepTemp = line.split(",")

  dayDB.append(dayTemp)
  dowDB.append(dowTemp)
  rhrDB.append(rhrTemp)
  slpDB.append(sleepTemp.rstrip('\n'))

print dayDB, dowDB, rhrDB, slpDB

# in the future, don't close the DB until it's updated
DBFileHandle.close()




#while databaseMatchFlag == 0:
  
for dow in dayRHR:
  print dow


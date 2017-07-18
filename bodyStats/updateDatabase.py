#! /usr/bin/env/python
import parseCSV

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

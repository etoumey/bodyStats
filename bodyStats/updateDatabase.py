#! /usr/bin/env/python
import parseCSV

# define the empty lists
dayRHR = []
daySlp = []
dayStp = []
rhr    = []
sleep  = []
steps  = []

parseCSV.parseRHR(dayRHR, rhr)


parseCSV.parseSleep(daySlp, sleep)

parseCSV.parseStep(dayStp, steps)

print dayRHR, rhr

print daySlp, sleep

print dayStp, steps

def parseRHR():

  # define the empty lists
  day = []
  rhr = []

  # open a sample file and ignore the first two lines (headers)
  f = open('rhr_29apr2017.csv', 'r')
  rhrData = f.readlines()[2:]

  # loop over the file lines and parse the data
  for line in rhrData:
    dayTemp, rhrTemp = line.split(",")

    day.append(dayTemp)
    rhr.append(rhrTemp.rstrip('\n'))


  print day, rhr

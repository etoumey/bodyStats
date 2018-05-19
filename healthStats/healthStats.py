import csv


class healthDatabase():
    '''This class contains the data structure for the health data as well as
       methods to import, print, and analyze the data.'''

    def __init__(self, databaseFilename):
        '''Upon instantiation of this object, automatically load the external
           health data from the database *.csv file.'''

        self.source = databaseFilename

        self.loadExternalData()

    def loadExternalData(self):
        '''Open an existing *.csv file that contains, column-wise: 
               Date:  YYYYMMDD
               Steps
               Sleep: hrs
               RHR:   bpm'''

        with open(self.source, 'r') as f:
            # Assume the file exists. Create a csv reader object that contains
            # the information from the file
            reader = csv.reader(f)

            # Assume the first row is a column header and skip
            headers = next(reader)

            rawData = {}

            for row in reader:
                dateKey = row[0]
                # Add duplicate row handling here
                rawData[dateKey] = row[1:]

        self.rawData = rawData

    def printDatabase(self):

        for row in self.rawData:
            print("Date: %s" % row)
            print(self.rawData[row])


def main():
    '''Main driver function'''

    healthDbJt = healthDatabase('userDb/database.csv')

    healthDbJt.printDatabase()

    
if __name__ == "__main__":
    main()

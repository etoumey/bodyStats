import csv


class healthDatabase():
    '''This class contains the data structure for the health data as well as
       methods to import, print, and analyze the data.'''

    def __init__(self, databaseFilename):
        '''Upon instantiation of this object, automatically load the external
           health data from the database *.csv file.'''

        self.source = databaseFilename
        self.rawData = {}

        self.loadExternalData()


    def loadExternalData(self):
        '''Open an existing *.csv file that contains, column-wise: 
               Date:  YYYYMMDD
               Steps
               Sleep: hrs
               RHR:   bpm'''

        with open(self.source, 'r') as dbFile:
            # Assume the file exists. Create a csv reader object that contains
            # the information from the file
            reader = csv.reader(dbFile)

            # Assume the first row is a column header and skip
            headers = next(reader)

            for row in reader:
                dateKey = row[0]
                # Add duplicate row handling here
                self.rawData[dateKey] = row[1:]


    def printDatabase(self):

        for row in self.rawData:
            print("Date: %s" % row)
            print(self.rawData[row])

    def getDailyData(self):
        dateQuery = input("Enter date query [YYYYMMDD]: ")

        #try:
        print(self.rawData[dateQuery])
        #except:
           # print("Date not present in DB...")


def main():
    '''Main driver function'''

    healthDbJt = healthDatabase('userDb/database.csv')

    healthDbJt.printDatabase()

    healthDbJt.getDailyData()

    
if __name__ == "__main__":
    main()

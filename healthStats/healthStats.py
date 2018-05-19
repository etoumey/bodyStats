import csv


class healthDatabase():
    '''Class containing the '''

    def __init__(self, databaseFilename):
        self.source = databaseFilename

        self.loadExternalData()

    def loadExternalData(self):
        ''''''
        with open(self.source, 'rb') as f:
            reader = csv.reader(f)

            headers = reader.next()

            print(headers)

            rawData = {}

            for h in headers:
                rawData[h] = []
            for r in reader:
                for h, v in zip(headers, r):
                    rawData[h].append(v)

            print(rawData)
            # 'workers', 'constant', 'age']
            # >>> column = {}
            # >>> for h in headers:
            # ...    column[h] = []
            # ...
            # >>> column
            # {'workers': [], 'constant': [], 'age': []}
            # >>> for row in reader:
            # ...   for h, v in zip(headers, row):
            # ...     column[h].append(v)





        #return(reader)
        self.rawData = reader

    def printDatabase(self):

        for row in self.rawData:
            print row


def main():
    '''Main driver function'''

    healthDbJt = healthDatabase('userDb/database.csv')

    #healthDbJt.printDatabase()

    
if __name__ == "__main__":
    main()

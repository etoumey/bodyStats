import reportFetch
import parser
import tripy
import plot


def bodyStats():

    # Wrapper for tripy: get keyboard input for desired action
    keyboardInputFlag = True

    while keyboardInputFlag:

        fetchAndParseFlag = input("Fetch new data from Garmin Connect? [y/n] ")

        if fetchAndParseFlag == 'y':
            reportFetch.reportFetch()
            parser.parser()
            tripy.tripy()

        elif fetchAndParseFlag == 'n':
            tripy.tripy()

        plotFlag = input("Generate new plot? [y/n] ")

        if plotFlag == 'y':
            plot.plot()

            keyboardInputFlag = False
    
        elif plotFlag == 'n':
            keyboardInputFlag = False

        else:
            continue

if __name__ == "__main__":
    bodyStats()

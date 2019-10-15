import reportFetch
import parser
import tripy
import plot

import sys


def bodyStats():

    keyboardInputFlag = True
    print(sys.argv)

    # Test if the user has supplied the appropriate key for cmd line args
    if sys.argv[1].startswith('-'):
        # -f: Fetch
        if 'f' in sys.argv[1]:
            print("Fetching reports...")
            reportFetch.reportFetch()

        if 'p' in sys.argv[1]:
            print("Parsing...")
            parser.parser()

        if 't' in sys.argv[1]:
            print("Running tripy...")
            tripy.tripy()

        if 'l' in sys.argv[1]:
            print("Plotting...")
            plot.main()

        keyboardInputFlag = False

    else:
        print("Invalid command line arguments. Continuing...")


    # Wrapper for tripy: get keyboard input for desired action


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

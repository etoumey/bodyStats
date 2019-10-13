import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from datetime import datetime, timedelta
from scipy.stats import gaussian_kde
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


def queryDB():
	#dateFormatDB = "%Y-%m-%d 00:00:00"
    connection = sqlite3.connect('userData.db')
    cursor = connection.cursor()
    sql = '''SELECT * from userData ORDER BY date ASC;'''
    data = cursor.execute(sql).fetchall()
    return data

class Plotter:
    """
    Class for producing various plots from garmin data.
    """
    def __init__(self):
        plt.rc('text', usetex=True)
        plt.rc('font', family='serif')
        data = queryDB()
        dateFormat = "%Y-%m-%d %H:%M:%S"
        self.dates = np.array([datetime.strptime(l[0], dateFormat) for l in data])
        self.RHR = np.array([l[1] for l in data])
        self.RHR = np.where(self.RHR==None, 0., self.RHR)
        self.sleep = np.array([l[2] for l in data])
        self.sleep = np.where(self.sleep==None, 0., self.sleep)
        self.stress = np.array([l[3] for l in data])
        self.stress = np.where(self.stress==None, 0., self.stress)
        self.ATL = np.array([l[4] for l in data])
        self.ATL = np.where(self.ATL==None, 0., self.ATL)
        self.CTL = np.array([l[5] for l in data])
        self.CTL = np.where(self.CTL==None, 0., self.CTL)
        self.TSS = np.array([l[6] for l in data])
        self.TSS = np.where(self.TSS==None, 0., self.TSS)
        self.dist = np.array([l[7] for l in data])
        self.dist = np.where(self.dist==None, 0., self.dist)
        self.elev = np.array([l[8] for l in data])
        self.elev = np.where(self.elev==None, 0., self.elev)
        self.tTot = np.array([l[9] for l in data])
        self.tTot = np.where(self.tTot==None, 0., self.tTot)


    def plotRHR(self):
        endIndex = len(self.dates)
        startIndex = max(0, endIndex - 42)

        plotFormat = "%m/%d/%Y"
        fig = plt.figure()
        axis = fig.add_subplot(2,1,1)
        axis.xaxis.set_major_formatter(DateFormatter(plotFormat))
        plt.plot(self.dates[startIndex:endIndex], self.RHR[startIndex:endIndex])
        plt.grid()
        plt.xlabel(r'\textbf{Time}')
        plt.ylabel(r'\textbf{RHR}')
        plt.title(r'\textbf{Resting Heart Rate}')
        axis = fig.add_subplot(2,1,2)
        axis.xaxis.set_major_formatter(DateFormatter(plotFormat))
        plt.plot(self.dates[startIndex:endIndex], self.stress[startIndex:endIndex])
        plt.grid()
        plt.xlabel(r'\textbf{Time}')
        plt.ylabel(r'\textbf{Stress}')
        plt.title(r'\textbf{Stress}')

        histRHR = list(filter(None, self.RHR))
        iqr = np.subtract(*np.percentile(histRHR, [75, 25])) # interquartile range
        nbins = int((max(histRHR)-min(histRHR))/(2.0*iqr/(len(histRHR)**(1.0/3.0)))) #Freedman-Diaconis rule for number of bins in histogram
        plt.figure()
        kde = gaussian_kde(histRHR)
        x = np.linspace(min(histRHR)-10, max(histRHR)+10, 500)
        pdf = kde.evaluate(x)
        currentAxis = plt.gca()
        currentAxis.plot(x, pdf)
        plt.hist(histRHR,density=1, bins = nbins)
        plt.title(r'\textbf{RHR Histogram and PDF}')
        plt.ylim((0,max(pdf)*1.5))

        fig = plt.figure()
        axis = fig.add_subplot(1,1,1)
        #axis.xaxis.set_major_formatter(DateFormatter(plotFormat))
        plt.scatter(self.stress[startIndex:endIndex], self.RHR[startIndex:endIndex])
        plt.grid()
        plt.xlabel(r'\textbf{Time}')
        plt.ylabel(r'\textbf{RHR}')
        plt.title(r'\textbf{Resting Heart Rate}')

        fig = plt.figure()
        #plt.plot(self.dates[startIndex:endIndex], self.ATL[startIndex:endIndex])
        #plt.plot(self.dates[startIndex:endIndex], self.CTL[startIndex:endIndex])
        ax1 = fig.add_subplot(1,1,1)
        ax1.xaxis.set_major_formatter(DateFormatter('%m/%d'))
        ax1.bar(self.dates[startIndex:endIndex], self.TSS[startIndex:endIndex], color='0.785', label='TSS')
        plt.ylabel(r'\textbf{TSS}')
        ax2 = ax1.twinx()
        ax2.plot(self.dates[startIndex:endIndex], np.subtract(self.ATL[startIndex:endIndex], self.CTL[startIndex:endIndex]), label=r'\textbf{TSB}')
        ax2.plot(self.dates[startIndex:endIndex], self.ATL[startIndex:endIndex], label=r'\textbf{ATL}')
        ax2.plot(self.dates[startIndex:endIndex], self.CTL[startIndex:endIndex], label=r'\textbf{CTL}')
        plt.grid()
        plt.xlabel(r'\textbf{Time}')
        plt.ylabel(r'\textbf{Training Load}')
        plt.title(r'\textbf{Performance Manager Chart}')
        plt.legend(loc=2)
        plt.savefig('activityArchive/src/PMC.pdf')
        plt.show()


    def plotCumulativeActivityYear(self, quantity='distance', year=2019, annotate=True, show=True, ax=None, saveFile=None):
        """
        Plot cumulative activity quantity as a function of days since Jan 1 for a
        given year.

        quantity: Activity quantity to plot. Must be either 'distance', 'time',
                  or 'elev'
        year: Year to plot data for
        annotate: Add features such as dividing lines for months, etc. to plot
        show: Whether or not to show plot. Set to False if plotting
              more data over top
        ax: matplotlib axis object to plot data onto
        saveFile: Location for plot to be saved. If None, plot is not saved.
        """
        if quantity == 'distance':
            quantityArr = self.dist
        elif quantity == 'time':
            quantityArr = self.tTot
        elif quantity == 'elev':
            quantityArr = self.elev
        else:
            raise ValueError("quantity must be one of 'distance', 'time', or 'elev'")


        if ax == None:
            fig, ax = plt.subplots()
        yearFilter = [date.year == year for date in self.dates]


        if not any(yearFilter):
            raise ValueError('No activities were found for %i' % year)

        yearDates = self.dates[yearFilter]
        yearFilteredQuantity = quantityArr[yearFilter]
        plotQuantity = np.where(yearFilteredQuantity==None, 0., yearFilteredQuantity)


        if yearDates[0] != datetime(year, 1, 1):
            numDays = (yearDates[0] - datetime(year, 1, 1)).days
            plotQuantity = np.append(np.zeros((numDays)), plotQuantity)

        cumulativeQuantity = np.cumsum(plotQuantity)
        plotDays = np.arange(1, 366)


        if (year % 4) == 0: #add "half-day" on Feb 29 for leap year
            plotDays = np.insert(plotDays.astype(float), 59, 59.5)

        if yearDates[-1] != datetime(year, 12, 31):
            currentDOY = (yearDates[-1] - datetime(year, 1, 1)).days
            plotDays = plotDays[:currentDOY+1]
            cumulativeQuantity = cumulativeQuantity[:currentDOY+1]

        plt.plot(plotDays, cumulativeQuantity, label=str(year))

        if annotate:
            for month in np.arange(1, 13):
                dayToPlot = (datetime(year,month,1)-datetime(year,1,1)).days
                plt.axvline(dayToPlot, c='black', linestyle=':', linewidth=1, alpha=0.5)
                plt.text(dayToPlot + 10, 1.12*max(cumulativeQuantity), datetime(year,month,1).strftime('%b'))

            plt.xlim(1, 365)
            plt.ylim(0, 1.1*max(cumulativeQuantity))
            plt.minorticks_on()
            ax.tick_params(which='both', direction='in', right=True)
            plt.xlabel('Days into year')
            
            if quantity == 'distance':
                plt.ylabel('Distance (miles)')
            elif quantity == 'time':
                plt.ylabel('Time (hours)')
            elif quantity == 'elev':
                plt.ylabel('Elevation Gain (feet)')
            
            plt.legend(loc=4)
        
        if saveFile != None:
            plt.savefig(saveFile)
        if show:
            plt.show()


    def plotCumulativeActivity(self, quantity='distance', ax=None, saveFile=None):
        """
        Plots cumulative activity quantity for all years up to present day.

        quantity: Activity quantity to plot. Must be either 'distance', 'time',
                  or 'elev'
        ax: Matplotlib object to plot data onto
        saveFile: Location for plot to be saved. If None, plot is not saved.
        """
        if ax == None:
            fig, ax = plt.subplots()

        startYear = min([date.year for date in self.dates])

        for year in np.arange(startYear, datetime.today().year+1):
            
            if year != datetime.today().year:
                self.plotCumulativeActivityYear(quantity=quantity, year=year, annotate=False, show=False, ax=ax)
            else:
                if saveFile != None:
                    self.plotCumulativeActivityYear(quantity=quantity, year=year, annotate=True, show=True, ax=ax, saveFile=saveFile)
                else:
                    self.plotCumulativeActivityYear(quantity=quantity, year=year, annotate=True, show=True, ax=ax)


    def plotActivityYear(self, quantity='distance', year=2019, annotate=True, show=True, ax=None, saveFile=None):
        """
        Plot activity quantity per day as a function of days since Jan 1 for a
        given year.

        quantity: Activity quantity to plot. Must be either 'distance', 'time',
                  or 'elev'
        year: Year to plot data for
        annotate: Add features such as dividing lines for months, etc.
                  to plot
        show: Whether or not to show plot. Set to False if plotting
              more data over top
        ax: Matplotlib axis object to plot data onto
        saveFile: Location for plot to be saved. If None, plot is not saved.
        """
        if quantity == 'distance':
            quantityArr = self.dist
        elif quantity == 'time':
            quantityArr = self.tTot
        elif quantity == 'elev':
            quantityArr = self.elev
        else:
            raise ValueError("quantity must be one of 'distance', 'time', or 'elev'")

        if ax == None:
            fig, ax = plt.subplots()

        yearFilter = [date.year == year for date in self.dates]
        
        if not any(yearFilter):
            raise ValueError('No activities were found for %i' % year)
        
        yearDates = self.dates[yearFilter]
        yearFilteredQuantity = quantityArr[yearFilter]
        plotQuantity = np.where(yearFilteredQuantity==None, 0., yearFilteredQuantity)
        
        if yearDates[0] != datetime(year, 1, 1):
            numDays = (yearDates[0] - datetime(year, 1, 1)).days
            plotQuantity = np.append(np.zeros((numDays)), plotQuantity)
        
        plotDays = np.arange(1, 366)
        
        if (year % 4) == 0: #add "half-day" on Feb 29 for leap year
            plotDays = np.insert(plotDays.astype(float), 59, 59.5)
        
        if yearDates[-1] != datetime(year, 12, 31):
            currentDOY = (yearDates[-1] - datetime(year, 1, 1)).days
            plotDays = plotDays[:currentDOY+1]
            plotQuantity = plotQuantity[:currentDOY+1]
        
        plt.plot(plotDays, plotQuantity, label=str(year))
        
        if annotate:
            for month in np.arange(1, 13):
                dayToPlot = (datetime(year,month,1)-datetime(year,1,1)).days
                plt.axvline(dayToPlot, c='black', linestyle=':', linewidth=1, alpha=0.5)
                plt.text(dayToPlot + 10, 1.12*max(plotQuantity), datetime(year,month,1).strftime('%b'))

            plt.xlim(1, 365)
            plt.ylim(0, 1.1*max(plotQuantity))
            plt.minorticks_on()
            ax.tick_params(which='both', direction='in', right=True)
            plt.xlabel('Days into year')

            if quantity == 'distance':
                plt.ylabel('Distance (miles)')
            elif quantity == 'time':
                plt.ylabel('Time (hours)')
            elif quantity == 'elev':
                plt.ylabel('Elevation Gain (feet)')

            plt.legend(loc=4)
        
        if saveFile != None:
            plt.savefig(saveFile)
        if show:
            plt.show()


    def plotActivity(self, quantity='distance', ax=None, saveFile=None):
        """
        Plots activity quantity per day for all years up to present day.

        quantity: Activity quantity to plot. Must be either 'distance', 'time',
                  or 'elev'
        ax: Matplotlib object to plot data onto
        saveFile: Location for plot to be saved. If None, plot is not saved.
        """
        if ax == None:
            fig, ax = plt.subplots()
        startYear = min([date.year for date in self.dates])
        for year in np.arange(startYear, datetime.today().year+1):
            if year != datetime.today().year:
                    self.plotActivityYear(quantity=quantity, year=year, annotate=False, show=False, ax=ax)
            else:
                if saveFile != None:
                    self.plotActivityYear(quantity=quantity, year=year, annotate=True, show=True, ax=ax, saveFile=saveFile)
                else:
                    self.plotActivityYear(quantity=quantity, year=year, annotate=True, show=True, ax=ax)


plotter = Plotter()
fig, ax = plt.subplots(figsize=(10,5))
#plotter.plotCumulativeActivity(quantity='elev', ax=ax)
fig, ax = plt.subplots(figsize=(10,5))
#plotter.plotActivity(quantity='elev', ax=ax)
plotter.plotRHR()


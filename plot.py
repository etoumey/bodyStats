import sqlite3
from datetime import datetime
from matplotlib import pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.patches import Rectangle
import numpy as np
from scipy.stats import gaussian_kde


def queryDB():
	connection = sqlite3.connect('userData.db')
	cursor = connection.cursor()

	sql = '''SELECT * from userData ORDER BY date ASC;'''
	data = cursor.execute(sql).fetchall()
	return data


def plotRHR(data):
	plt.rc('text', usetex=True)
	plt.rc('font', family='serif')

	dateFormat = "%Y-%m-%d %H:%M:%S"
	plotFormat = "%m/%d/%Y"
	dates = [l[0] for l in data]
	dates = [datetime.strptime(d, dateFormat) for d in dates]
	#dates = [datetime.strptime(d, dateFormat).strftime(plotFormat) for d in dates]
	RHR = [l[1] for l in data]
	Stress = [l[3] for l in data]
	Sleep = [l[2] for l in data]
	ATL = [l[4] for l in data]
	CTL = [l[5] for l in data]
	Dist = [l[7] for l in data]
	Elev = [l[8] for l in data]
	tTot = [l[9] for l in data]


	endIndex = len(dates) 
	if endIndex > 120:
		startIndex = endIndex - 120
	else:
		startIndex = 0


	fig = plt.figure()
	axis = fig.add_subplot(2,1,1)
	axis.xaxis.set_major_formatter(DateFormatter(plotFormat))
	plt.plot(dates[startIndex:endIndex], RHR[startIndex:endIndex])
	plt.grid()
	plt.xlabel(r'\textbf{Time}')
	plt.ylabel(r'\textbf{RHR}')
	plt.title(r'\textbf{Resting Heart Rate}')
	
	axis = fig.add_subplot(2,1,2)
	axis.xaxis.set_major_formatter(DateFormatter(plotFormat))
	plt.plot(dates[startIndex:endIndex], Stress[startIndex:endIndex])
	plt.grid()
	plt.xlabel(r'\textbf{Time}')
	plt.ylabel(r'\textbf{Stress}')
	plt.title(r'\textbf{Stress}')

	histRHR = list(filter(None, RHR))

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
	plt.scatter(Stress[startIndex:endIndex], RHR[startIndex:endIndex])
	plt.grid()
	plt.xlabel(r'\textbf{Time}')
	plt.ylabel(r'\textbf{RHR}')
	plt.title(r'\textbf{Resting Heart Rate}')

	fig = plt.figure()
	plt.plot(dates[startIndex:endIndex], ATL[startIndex:endIndex])
	plt.plot(dates[startIndex:endIndex], CTL[startIndex:endIndex])
	plt.show(block=True)



def main():
	data = queryDB()
	plotRHR(data)




if __name__ == "__main__":
	main()
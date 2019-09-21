import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class activityPlotter:
    """
    Class for producing various plot from activity data. Requires exported CSV
    file from https://connect.garmin.com/modern/activities
    """
    def __init__(self, filename='Activities.csv'):
        self.filename = filename
        self.data = pd.read_csv(filename)
        self.dates = np.array([datetime.strptime(date, '%Y-%m-%d %X').date()\
                      for date in self.data['Date']])
        self.distances = np.array(self.data['Distance'])
        self.elapsed_times = np.array(self.data['Time'])
        self.elapsed_times = np.array([np.dot([1., 1./60., 1./3600.],\
                              np.array(time.split(':')).astype('float'))\
                              for time in self.elapsed_times])
        self.elevation_gains = np.array(self.data['Elev Gain'])
        self.elevation_gains[np.where(self.elevation_gains == '--')] = 0.0
        self.elevation_gains = np.array([float(str(num).replace(',', ''))\
                                         for num in self.elevation_gains])

    def plot_cumulative_quantity_year(self, quantity='distance', year=2019,\
                                      annotate=True, show=True, ax=None, save_file=None):
        """
        Plot cumulative activity quantity as a function of days since Jan 1 for a
        given year.

        quantity: Activity quantity to plot. Must be either 'distance', 'time',
                  or 'elev_gain'
        year: Year to plot data for
        annotate: Add features such as dividing lines for months, etc.
                  to plot
        show: Whether or not to show plot. Set to False if plotting
              more data over top
        ax: matplotlib axis object to plot data onto
        save_file: Location for plot to be saved. If None, plot is not saved.
        """
        if quantity == 'distance':
            quantity_arr = self.distances
        elif quantity == 'time':
            quantity_arr = self.elapsed_times
        elif quantity == 'elev_gain':
            quantity_arr = self.elevation_gains
        else:
            raise ValueError("quantity must be one of 'distance', 'time', or 'elev_gain'")
        if ax == None:
            fig, ax = plt.subplots()
        year_filter = [date.year == year for date in self.dates]
        if not any(year_filter):
            raise ValueError('No activities were found for %i' % year)
        year_dates = self.dates[year_filter]
        year_filtered_quantity = quantity_arr[year_filter]
        plot_quantity = np.zeros((365,))
        day_counter = datetime(year, 1, 1)
        for i in np.arange(365):
            if day_counter.date() in year_dates:
                day_idx = np.where(year_dates == day_counter.date())
                plot_quantity[i] = np.sum(year_filtered_quantity[day_idx])
            day_counter += timedelta(days=1)
        cumulative_quantity = np.cumsum(plot_quantity)
        plot_days = np.arange(1, 366)
        if datetime.today().year == year:
            current_days_into_year = (datetime.today().date() -\
                                      datetime(year, 1, 1).date()).days
            plot_days = plot_days[:current_days_into_year+1]
            cumulative_quantity = cumulative_quantity[:current_days_into_year+1]
        plt.plot(plot_days, cumulative_quantity, label=str(year))
        if annotate:
            for month in np.arange(1, 13):
                day_to_plot = (datetime(year,month,1)-datetime(year,1,1)).days
                plt.axvline(day_to_plot, c='black', linestyle=':',\
                            linewidth=1, alpha=0.5)
                plt.text(day_to_plot + 10, 1.12*max(cumulative_quantity),\
                         datetime(year,month,1).strftime('%b'))
            plt.xlim(1, 365)
            plt.ylim(0, 1.1*max(cumulative_quantity))
            plt.minorticks_on()
            ax.tick_params(which='both', direction='in', right=True)
            plt.xlabel('Days into year')
            if quantity == 'distance':
                plt.ylabel('Distance (miles)')
            elif quantity == 'time':
                plt.ylabel('Time (hours)')
            elif quantity == 'elev_gain':
                plt.ylabel('Elevation Gain (feet)')
            plt.legend(loc=4)
        if save_file != None:
            plt.savefig(save_file)
        if show:
            plt.show()


    def plot_cumulative_quantity(self, quantity='distance', ax=None,\
                                 save_file=None):
        """
        Plots cumulative activity quantity for all years up to present day.

        quantity: Activity quantity to plot. Must be either 'distance', 'time',
                  or 'elev_gain'
        ax: Matplotlib object to plot data onto
        save_file: Location for plot to be saved. If None, plot is not saved.
        """
        if ax == None:
            fig, ax = plt.subplots()
        start_year = min([date.year for date in self.dates])
        for year in np.arange(start_year, datetime.today().year+1):
            if year != datetime.today().year:
                try:
                    self.plot_cumulative_quantity_year(quantity=quantity, year=year,\
                                                       annotate=False, show=False, ax=ax)
                except ValueError:
                    print('No data found for %i' % year)
            else:
                if save_file != None:
                    self.plot_cumulative_quantity_year(quantity=quantity, year=year,\
                                                       annotate=True, show=True, ax=ax,\
                                                       save_file=save_file)
                else:
                    self.plot_cumulative_quantity_year(quantity=quantity, year=year,\
                                                       annotate=True, show=True, ax=ax)

    def plot_quantity_year(self, quantity='distance', year=2019, annotate=True,\
                           show=True, ax=None, save_file=None):
        """
        Plot activity quantity per day as a function of days since Jan 1 for a
        given year.

        quantity: Activity quantity to plot. Must be either 'distance', 'time',
                  or 'elev_gain'
        year: Year to plot data for
        annotate: Add features such as dividing lines for months, etc.
                  to plot
        show: Whether or not to show plot. Set to False if plotting
              more data over top
        ax: Matplotlib axis object to plot data onto
        save_file: Location for plot to be saved. If None, plot is not saved.
        """
        if quantity == 'distance':
            quantity_arr = self.distances
        elif quantity == 'time':
            quantity_arr = self.elapsed_times
        elif quantity == 'elev_gain':
            quantity_arr = self.elevation_gains
        else:
            raise ValueError("quantity must be one of 'distance', 'time', or 'elev_gain'")
        if ax == None:
            fig, ax = plt.subplots()
        year_filter = [date.year == year for date in self.dates]
        if not any(year_filter):
            raise ValueError('No activities were found for %i' % year)
        year_dates = self.dates[year_filter]
        year_filtered_quantity = quantity_arr[year_filter]
        plot_quantity = np.zeros((365,))
        day_counter = datetime(year, 1, 1)
        for i in np.arange(365):
            if day_counter.date() in year_dates:
                day_idx = np.where(year_dates == day_counter.date())
                plot_quantity[i] = np.sum(year_filtered_quantity[day_idx])
            day_counter += timedelta(days=1)
        plot_days = np.arange(1, 366)
        if datetime.today().year == year:
            current_days_into_year = (datetime.today().date() -\
                                      datetime(year, 1, 1).date()).days
            plot_days = plot_days[:current_days_into_year+1]
            plot_quantity = plot_quantity[:current_days_into_year+1]
        plt.plot(plot_days, plot_quantity, label=str(year))
        if annotate:
            for month in np.arange(1, 13):
                day_to_plot = (datetime(year,month,1)-datetime(year,1,1)).days
                plt.axvline(day_to_plot, c='black', linestyle=':',\
                            linewidth=1, alpha=0.5)
                plt.text(day_to_plot + 10, 1.12*max(plot_quantity),\
                         datetime(year,month,1).strftime('%b'))
            plt.xlim(1, 365)
            plt.ylim(0, 1.1*max(plot_quantity))
            plt.minorticks_on()
            ax.tick_params(which='both', direction='in', right=True)
            plt.xlabel('Days into year')
            if quantity == 'distance':
                plt.ylabel('Distance (miles)')
            elif quantity == 'time':
                plt.ylabel('Time (hours)')
            elif quantity == 'elev_gain':
                plt.ylabel('Elevation Gain (feet)')
            plt.legend(loc=4)
        if save_file != None:
            plt.savefig(save_file)
        if show:
            plt.show()

    def plot_quantity(self, quantity='distance', ax=None, save_file=None):
        """
        Plots activity quantity per day for all years up to present day.

        quantity: Activity quantity to plot. Must be either 'distance', 'time',
                  or 'elev_gain'
        ax: Matplotlib object to plot data onto
        save_file: Location for plot to be saved. If None, plot is not saved.
        """
        if ax == None:
            fig, ax = plt.subplots()
        start_year = min([date.year for date in self.dates])
        for year in np.arange(start_year, datetime.today().year+1):
            if year != datetime.today().year:
                try:
                    self.plot_quantity_year(quantity=quantity, year=year,\
                                            annotate=False, show=False, ax=ax)
                except ValueError:
                    print('No data found for %i' % year)
            else:
                if save_file != None:
                    self.plot_quantity_year(quantity=quantity, year=year,\
                                            annotate=True, show=True, ax=ax,\
                                            save_file=save_file)
                else:
                    self.plot_quantity_year(quantity=quantity, year=year,\
                                            annotate=True, show=True, ax=ax)


if __name__ == '__main__':
    activity_plotter = activityPlotter()
    fig, ax = plt.subplots(figsize=(10,5))
    activity_plotter.plot_cumulative_quantity(quantity='elev_gain', ax=ax)
    fig, ax = plt.subplots(figsize=(10,5))
    activity_plotter.plot_quantity(quantity='elev_gain', ax=ax)


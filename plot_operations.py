"""This module contains functions required to plot the data on the graphs"""
import logging
import matplotlib.pyplot as plt
class PlotOperations():
    """Creates plots of mean temperatures monthly or daily"""
    logging.basicConfig(filename="my_log_file.txt",
                        format='%(asctime)s - %(name)s - %(levelname)s- %(message)s',
                        filemode='w')
    def __init__(self):
        """Initializes the logger"""
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
    def create_boxplot(self, list_of_tuples, user_from_year, user_to_year):
        """Creates plots of mean temperatures monthly between 2 year ranges"""
        try:
            weather_data = {
                                '01': [],
                                '02': [],
                                '03': [],
                                '04': [],
                                '05': [],
                                '06': [],
                                '07': [],
                                '08': [],
                                '09': [],
                                '10':[],
                                '11':[],
                                '12':[]
                            }
            try:
                for row in list_of_tuples:
                    date = row[1]
                    month = str(date).split('-')[1]
                    mean_temp = row[5]
                    weather_data[month].append(mean_temp)
            except Exception as err:
                self.logger.error("PlotOperations: create_boxplot: loop: %s",err)
            jan = weather_data['01']
            feb = weather_data['02']
            march = weather_data['03']
            april = weather_data['04']
            may = weather_data['05']
            june = weather_data['06']
            july = weather_data['07']
            august = weather_data['08']
            september = weather_data['09']
            october = weather_data['10']
            nov = weather_data['11']
            dec = weather_data['12']
            columns = [jan, feb, march, april, may, june, july,
                       august, september, october, nov, dec]
            fig,axis = plt.subplots()
            axis.boxplot(columns)
            plt.title(f'Monthly Temperature Distribution for: {user_from_year} to {user_to_year}')
            plt.ylabel('Temperature(Celsius)')
            plt.xlabel('Month')
            plt.show()
        except Exception as err:
            self.logger.error("PlotOperations: create_boxplot: %s",err)
    def line_graph(self, records):
        """Creates line plots of mean temperatures for a month"""
        try:
            x_coordinate = []
            y_coordinate = []
            try:
                for items in records:
                    y_coordinate.append(items[5])
                    x_coordinate.append(items[1])
            except Exception as err:
                self.logger.error("PlotOperations: line_graph: loop: %s",err)         
            plt.plot(x_coordinate, y_coordinate)
            plt.tick_params(axis='x', rotation=45)
            plt.ylabel('Mean Temperatures \N{DEGREE SIGN}C')
            plt.xlabel('Days of the month')
            plt.title("Mean Temperatures for the Month")
            plt.grid()
            plt.show()
        except Exception as err:
            self.logger.error("PlotOperations: line_graph: %s",err)

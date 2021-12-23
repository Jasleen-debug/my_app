"""This module presents the user with a menu of choices"""
import logging
import urllib.request
import datetime
from scrape_weather import WeatherScrapper
from plot_operations import PlotOperations
from db_operations import DBOperations

class WeatherProcessor():
    """This class makes call to scraper, database and plot modules"""
    logging.basicConfig(filename="my_log_file.txt",
                        format='%(asctime)s - %(name)s - %(levelname)s- %(message)s',
                        filemode='w')
    def __init__(self):
        """Initializes the logger"""
        try:
            self.logger = logging.getLogger()
            self.logger.setLevel(logging.DEBUG)
            self.logger.info("Starting the program")
            self.db = DBOperations()
            self.plot = PlotOperations()
        except Exception as err:
            self.logger.error('init method: %s', err)
        
    def main(self):
        """Handle user operations of the weather app"""
        try:
            user_option = input ("Fetch all available weather data, only update existing, or skip? [F]ull/[U]pdate/[S]kip: ")

            self.update_option(user_option)

            self.user_temp_choice()

            check = input("Finished? [Y/N]: ")

            self.check_option(check)
            print("End the program")
            print("look i m here")     
        except Exception as err:
            self.logger.error('main method: %s', err)

    def scrape_data(self, update_condition):
        """The class contains our test of the above functions"""
        now = datetime.datetime.now()
        year = int(str(now).split('-')[0])
        month = int(str(now).split('-')[1])
        try:
            myparser = WeatherScrapper()
            url = f'https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=1&Year={myparser.year}&Month={myparser.month}#'
            with urllib.request.urlopen(url) as response:
                html = str(response.read())
            myparser.month_object = myparser.month
            myparser.year_object = myparser.year
            myparser.feed(html)
            myparser.update_month_check = update_condition
            check_update_condition = f'{myparser.year_object}-{myparser.month_object}'
            new_year = myparser.year
            new_month = myparser.month
            print(f'Started Processing: {new_year} - {new_month}')
            try:
                url_new = ''
                while response.getcode() == 200:
                    if update_condition ==check_update_condition:
                        break
                    new_month = new_month - 1
                    myparser.month_object = new_month
                    if new_month < 1:
                        new_month = 12
                        myparser.month_object = new_month
                        new_year = new_year - 1
                        myparser.year_object = new_year
                    url_new = f'https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=1&Year={new_year}&Month={new_month}#'
                    print(f'Started Processing: {new_year} - {new_month}')
                    with urllib.request.urlopen(url_new) as response:
                        html = str(response.read())
                    myparser.feed(html)
                    if myparser.month_object != myparser.all_months[myparser.title_month]:
                        break
            except Exception as err:
                self.logger.error('No more data could be found: %s', err)
            return myparser.print_all()
        except Exception as err:
            self.logger.error('scrape_data method: %s', err)
    def user_temp_choice(self):
        """This method gives the user the choice to plot a box or line graph"""
        try:
            user_plot = input("Plot monthly or daily data? [M/D]: ")
            if user_plot.lower() == 'm':
                from_year = input("Enter from year YYYY: ")
                to_year = input("Enter to year YYYY: ")
                rows_list = self.db.fetch_data_monthly(from_year, to_year)
                plot = self.plot.create_boxplot(rows_list, from_year, to_year)
            elif user_plot.lower() == 'd':
                month = input("Please enter a month in this format YYYY-MM: ")
                daily = self.db.fetch_data_daily(month)
                self.plot.line_graph(daily)
                print('Plot completed')
            else:
                print('Please enter either M or D')
        except Exception as err:
            self.logger.error('user_temp_choice method: %s', err)
    def update_option(self,user_option):
        """This method gives the user to scrape all data or only update missing"""
        try:
            if user_option.lower() == 'f':
                self.db.initialize_db()
                self.db.purge_data()
                my_dict = self.scrape_data('')
                self.db.initialize_db()
                self.db.save_data(my_dict)
            elif user_option.lower() == 'u':
                date = self.db.fetch_latest_date()
                year = date[0][0].split('-')[0]
                month = date[0][0].split('-')[1]
                update_from = f'{year}-{month}'
                my_dict = self.scrape_data(update_from)
##                self.db.initialize_db()
                self.db.save_data(my_dict)
        except Exception as err:
            self.logger.error('update_option method: %s', err)
    def check_option(self,check):
        """This method asks the user to continue or exit"""
        try:
            while check.lower() != "y":
                try:
                    self.user_temp_choice()
                    check = input("Finished? [Y/N]: ")
                    if check.lower == 'y':
                        self.logger.info("Ending the program")
                        break
                except Exception as err:
                    self.logger.error('check_option method:loop: %s', err)
        except Exception as err:
            self.logger.error('check_option method: %s', err)

if __name__ == '__main__':
    weather_ops = WeatherProcessor()
    weather_ops.main()




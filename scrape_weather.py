"""
Author: Chukswama Ogu
This module scrapes data feom the government of Canada website.
"""
from html.parser import HTMLParser
import datetime
import urllib.request
import logging
class WeatherScrapper(HTMLParser):
    """
    This class represents a collection of temperature data.
    """
    logging.basicConfig(filename="my_log_file.txt", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filemode='w')
    def __init__(self):
        """This method  initializes all the attributes used in scraping the data."""
        try:
            super().__init__()
            self.in_cell = False
            self.cell_index = -1
            self.daily_temps = {}
            self.weather = {}
            self.max_temp = ''
            self.min_temp = ''
            self.mean_temp = ''
            self.th_flag = False
            self.date_flag = ''
            self.th_flag_cell = -1
            self.year_object = ''
            self.month_object = ''
            self.title_flag = False
            self.title_year = ''
            self.title_month = ''
            self.update_month_check = ''
            self.now = datetime.datetime.now()
            self.year = int(str(self.now).split('-')[0])
            self.month = int(str(self.now).split('-')[1])
            self.all_weather = {}
            self.all_months = {"January": 1,
                        "February": 2,
                        "March": 3,
                        "April": 4,
                        "May": 5,
                        "June": 6,
                        "July": 7,
                        "August": 8,
                        "September": 9,
                        "October": 10,
                        "November": 11,
                        "December": 12}
            self.logger = logging.getLogger()
            self.logger.setLevel(logging.WARNING)
        except Exception as err:
            self.logger.error(f"__init__ method: {err}")
    def check_float(self, potential_float):
        """This method checks if the data received can be converted to a float"""
        try:
            float(potential_float)
            return True
        except ValueError:
            return False
    def handle_starttag(self, tag, attrs):
        """This method handles each start tag found on the website"""
        try:
            if tag == 'title':
                self.title_flag = True
            if tag == 'tbody':
                self.th_flag = True
            if tag == 'tr':
                self.cell_index = -1
            if tag == 'td':
                self.in_cell = True
                self.cell_index += 1
        except Exception as err:
            self.logger.error(f"Handle_Starttag method: {err}")
    def handle_endtag(self, tag):
        """This method handles each start tag found on the website"""
        try:
            if tag == 'title':
                self.title_flag = False
            if tag == 'td' or tag =='th':
                self.in_cell = False
            if tag == 'tbody':
                self.th_flag_cell += 1
        except Exception as err:
            self.logger.error(f"Handle_Endtag method: {err}")
    def handle_data(self, data):
        """This method handles the data in each tag found on the website"""
        try:
            check = self.check_float(data.strip())
            if self.title_flag:
                self.title_month = str(data.strip().split()[4])
                self.title_year = int(data.strip().split()[5])
                if self.month_object != self.all_months[self.title_month]:
                    return
            if self.th_flag and self.cell_index == -1 and check:
                if self.month_object != self.all_months[self.title_month]:
                    return
                self.date_flag = data.replace("\\n", "")
            if self.in_cell and self.cell_index == 0 and check:
                if self.month_object != self.all_months[self.title_month]:
                    return
                self.max_temp = float(data.strip())
                self.daily_temps = {"Max": self.max_temp,
                                    "Min": self.min_temp,
                                    "Mean": self.mean_temp}
            elif self.in_cell and self.cell_index == 1 and check:
                if self.month_object != self.all_months[self.title_month]:
                    return
                self.min_temp = float(data.strip())
                self.daily_temps = {"Max": self.max_temp,
                                    "Min": self.min_temp,
                                    "Mean": self.mean_temp}
            elif self.in_cell and self.cell_index == 2 and check:
                if self.month_object != self.all_months[self.title_month]:
                    return
                self.mean_temp  = float(data.strip())
                self.daily_temps = {"Max": self.max_temp,
                                    "Min": self.min_temp,
                                    "Mean": self.mean_temp}
            elif self.in_cell and self.cell_index == 3 and check:
                if self.month_object != self.all_months[self.title_month]:
                    return
                self.weather[f'{self.year_object}-{self.month_object:02d}-{self.date_flag}'] = self.daily_temps
                self.all_weather[ self.date_flag] = self.daily_temps
        except ValueError as err:
            self.logger.error(f"Handle_Data method: {err}")
    def print_all(self):
        """This method prints all the temperatures with associated dates"""
        try:
            #print(self.weather)
            return self.weather
        except Exception as err:
            self.logger.error(f"Print_All method: {err}")

"""This module handles all the database operations."""
"""Author: Jasleen Kaur"""
import logging
from dbcm import DBCM
class DBOperations():
    """The class contains functions to store and retrieve the data."""
    logging.basicConfig(filename="my_log_file.txt",
                        format='%(asctime)s - %(name)s - %(levelname)s- %(message)s',
                        filemode='w')
    def __init__(self):
        """Initializes the database name"""
        self.db_name = "weather.sqlite"
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.WARNING)
    def initialize_db(self):
        """Creates the database table"""
        with DBCM(self.db_name) as cursor:
            try:
                cursor.execute("""create table if not exists weatherData
                                (id integer primary key autoincrement not null,
                                sample_date text not null,
                                location text not null,
                                max_temp real not null,
                                min_temp real not null,
                                avg_temp real not null);""")
            except Exception as err:
                self.logger.error("DBOperations: initialize_db method: %s",err)
    def save_data(self, my_dict):
        """Takes dict of dicts and saves only the unique data into database"""
        with DBCM(self.db_name) as cursor:
            try:
                for key,value in my_dict.items():
                    cursor.execute("""SELECT sample_date FROM weatherData
                                   WHERE sample_date=?""", (key,))
                    result = cursor.fetchone()
                    if result:
                        print(key)
                        print("Record with this date already exists!")
                    else:
                        values = value.values()
                        values_list = list(values)
                        try:
                            sql="""INSERT INTO weatherData
                                (sample_date,location,max_temp,min_temp,avg_temp)
                                values (?,?,?,?,?)"""
                            data=(key,'Winnipeg,MB',values_list[0],values_list[1],values_list[2])
                            cursor.execute(sql,data)
                        except Exception as err:
                            self.logger.error("DBOperations: save_data: loop: %s",err)
            except Exception as err:
                self.logger.error("DBOperations: save_data: %s",err)
    def purge_data(self):
        """Deletes all records in the database"""
        with DBCM(self.db_name) as cursor:
            cursor.execute("""DELETE FROM weatherData """)
    def fetch_data_daily(self, user_input):
        """Returns data for each day of a given month only"""
        with DBCM(self.db_name) as cursor:
            try:
                cursor.execute("""SELECT * FROM weatherData
                               WHERE sample_date LIKE ?""", (user_input+'%',) )
                rows_list = cursor.fetchall()
                return rows_list
            except Exception as err:
                self.logger.error("DBOperations: fetch_data_daily: %s",err)
    def fetch_data_monthly(self, from_year, to_year):
        """Returns the data for each month for each year given as input"""
        with DBCM(self.db_name) as cursor:
            try:
                cursor.execute("""SELECT * FROM weatherData
                               WHERE date(sample_date) >= ? AND date(sample_date)<= ?
                               ORDER BY date(sample_date) ASC""",
                              (from_year+'-01-01',to_year+'-12-31',))
                rows_list = cursor.fetchall()
                return rows_list
            except Exception as err:
                self.logger.error("DBOperations: fetch_data_monthly: %s",err)
    def fetch_latest_date(self):
        """This function retrieves the latest date from the database."""
        with DBCM(self.db_name) as cursor:
            try:
                cursor.execute("""SELECT MAX(date(sample_date)) FROM weatherData""")
                latest_date = cursor.fetchall()
                return latest_date
            except Exception as err:
                self.logger.error("DBOperations: fetch_latest_date: %s",err)

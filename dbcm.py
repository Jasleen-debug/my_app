"""sqlite3 module allows us to use the database functionality in our program"""
import sqlite3
class DBCM():
    """This is the context manager class that lets us extend"""
    """the with statement to work with database"""
    def __init__(self,db_name ):
        """Initializes the database connection and the cursor object"""
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
    def __enter__(self):
        """Returns the cursor object to the with statement of the context manager"""
        return self.cur
    def __exit__(self, exc_type, exc_value, exc_trace):
        """Saves the changes to the database, closes the cursor and database sconnection"""
        self.conn.commit()
        self.cur.close()
        self.conn.close()

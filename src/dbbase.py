import sys
import mariadb
from config import Cfg
from typing import Tuple


class Db(Cfg):

    rz_conn = None # TO-DO: make a typing on db Connection
    gz_conn = None # TO-DO: make a typing on db Connection


    def __init__(self):
        """
        Create an instance of the configurationfile
        """
        super(Db, self).__init__()
        self.gz_conn = self._db_conn(user=self.user, password=self.password, 
                                    host=self.host, port_str=self.port, 
                                    database=self.gz_db)
        self.rz_conn = self._db_conn(user=self.user, password=self.password, 
                                    host=self.host, port_str=self.port, 
                                    database=self.rz_db)

    def _db_conn(self, user:str, password:str, host:str, port_str:str, database:str):
        """
        Establish connection to mariadb platform
        """
        try:
            conn = mariadb.connect(
                user=user,
                password=password,
                host=host,
                port=int(port_str),
                database=database)
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
        return conn

    def get_devices_all(self):
        # Get Cursor
        cur = self.gz_conn.cursor()
        # Read devices of database
        cur.execute("SELECT * FROM device")
        result = cur.fetchall()
        return result
    
    def get_device_data_by_name(self, device_name:str):
        # Get Cursor
        cur = self.gz_conn.cursor() # TO-DO: typing for cursor variable
        # Read devices of database
        query:str = f"SELECT * FROM device WHERE name = '{device_name}'"
        
        cur.execute(query)
        r = cur.fetchone() # TO-DO: typing this tuple
      
        d = {
            "name": r[1], "brand": r[2], "model": r[3], 
            "ext_device_id":r[4], "url": r[5], "access_token":r[6]
            }

        return d
        
    def write_climate_logger_device_data(self):
        pass


if __name__ == "__main__":
    B = Db()
    print(B.get_device_data_by_name("climate-logger-01"))
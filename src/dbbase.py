import sys
import time
from datetime import datetime
from time import mktime
from typing import List, Tuple

import mariadb

from config import Cfg


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

    def get_device_variables_by_name(self, device_name:str):
        # Get Cursor
        result:List[str] = []
        cur = self.gz_conn.cursor()

        query = f"""
            SELECT v.name
            FROM device d, variable v, device_variable dv
            WHERE
            d.device_id = dv.device_id
            and dv.variable_id = v.variable_id
            AND d.name = '{device_name}'
            """
        # Read devices of database
        cur.execute(query)
        query_result = cur.fetchall()
        for item in query_result:
            result.append(item[0])
        # Convert to list

        return result

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

    def write_climate_logger_device_data(self, ext_device_id:str, timestamp_str:str, temperature:int, humidity:int):

        # convert timestap to datetime
        timestamp:datetime = datetime.fromtimestamp(mktime(time.strptime(timestamp_str, "%a %b %d %H:%M:%S %Y")))
  
        # Get Cursor
        cur = self.rz_conn.cursor()
        query:str = f"""
        INSERT INTO climatedata (ext_device_id, timestamp, temperature, humidity)
        VALUES ('{ext_device_id}', '{timestamp.strftime('%Y-%m-%d %H:%M:%S')}', {float(temperature)}, {float(humidity)})
        """
        cur.execute(query)
        cur.execute("COMMIT")


if __name__ == "__main__":
    B = Db()
    ext_device_id = '36003b000e47353136383631'
    timestamp = "Sun Feb 7 14:44:25 2021"


    temperature = 21
    humidity = 30

    B.write_climate_logger_device_data(ext_device_id, timestamp, temperature, humidity)
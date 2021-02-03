import json
import requests 
import mariadb
import sys
from config import Cfg
from particle.particle import Particle
from typing import Dict, Any
from dbbase import Db

class DeviceScraper(Cfg):
    """
    Classfor scraping data of iot devices.
    """

    url:str = ""
    access_token:str = ""
    device_id:str = ""

    def __init__(self):
        super(DeviceScraper, self).__init__()
        # self._read_device_var()

    def _read_device_var(self, device_name:str):
        """
        Read device variables off particle.io
        """

        device_info:Dict[str, str] = Db().get_device_data_by_name(device_name)
        url:str = device_info["url"] 
        ext_device_id:str = device_info["ext_device_id"]
        access_token:str = device_info["access_token"]

        request_url = url + ext_device_id + "/measure/?access_token=" + access_token
        response:Dict[str, Any] = json.loads(requests.get(request_url).text)
    
        return response




        

    # Get Cursor
    # cur = conn.cursor()
    # cur.execute("INSERT INTO devices (id) Values ()")
    # cur.execute("commit;")




if __name__ == "__main__":
    # SCRAPER = DeviceScraper()
    # DEVICE = SCRAPER._get_device()
    # print(DEVICE)

    SCRAPER = DeviceScraper()
    RESULT = SCRAPER._read_device_var("climate-logger-01")
    print(RESULT)
    print(type(RESULT))

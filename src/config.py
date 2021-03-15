import json
import os
from typing import Dict


class Cfg:
    """
    Objective is to provide a module that makes config variables easily accessible
    """

    user: str = None
    password: str = None
    host: str = None
    port: str = None
    rz_db: str = None
    gz_db: str = None

    def __init__(self):
        self._read_config()

    def _cfg_select(self):
        """
        Check if config file exist.
        if not try to copy the copy conf.json into repo.
        """
        response: bool = os.path.isfile("conf.json")

        if response == False:
            raise FileNotFoundError

        return "conf.json"

    def _get_conf_dict(self):
        """
        Code to return actual values in the file
        """
        f = open(self._cfg_select(), "r")
        json_str: str = f.read()
        d: Dict[str, str] = json.loads(json_str)
        return d

    def _read_config(self):
        """
        Update class variables
        """
        d = self._get_conf_dict()
        self.user = d["user"]
        self.password = d["password"]
        self.host = d["host"]
        self.port = d["port"]
        self.rz_db = d["rawzone"]["database"]
        self.gz_db = d["goldzone"]["database"]

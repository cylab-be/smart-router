#!/usr/bin/python3
import datetime
import threading
from os.path import join, dirname
from dotenv import load_dotenv
from scapy.all import *
from scapy.layers.dns import DNS, DNSRR
from scapy.layers.inet import IP
from scapy.layers.inet import Ether
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
#import pymysql
from python.httpquery import httpquery
from python.database import database


class firstActivityFaker :

    def run(self):
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        self.logfile = os.environ.get("LOGFILE")
        logging.basicConfig(filename=self.logfile, level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s - %(message)s')
        self.db = database()
        self.db.connect()
        self.db.insertFakeHTTPQueriesBeforeFirstActivity()



if __name__ == "__main__":
    firstActivityFaker().run()

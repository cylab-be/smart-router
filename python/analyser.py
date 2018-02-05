#!/usr/bin/python3
import datetime
import threading
from os.path import join, dirname

import pymysql
from python.database import database
from dotenv import load_dotenv
from scapy.all import *
from scapy.layers.dns import DNS, DNSRR
from scapy.layers.inet import IP
from scapy.layers.inet import Ether

class analyser (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        pymysql.install_as_MySQLdb()
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        self.logfile = os.environ.get("LOGFILE")
        logging.basicConfig(filename=self.logfile, level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s - %(message)s')
        self.db = database()
        self.db.connect()

    def run(self):
        logging.info("run analyser")
        macAddresses = self.getAllHosts()

        # macAddresses = ('08:00:27:54:8b:1b',':8b:1b','08:008b:1b','08:00:27:')
        # logging.debug(macAddresses)

        for mac in macAddresses :
            # logging.debug(mac)
            self.checkHostAndAddItIfNotPresent(mac)

    def getAllHosts(self):

        if self.db.connection == "sqlite":
            sql = "select mac_iot from HTTPQueries"
        elif self.db.connection == "mysql":
            sql = "SELECT mac_iot FROM HTTPQueries"
        ret = self.db.execquery(sql)

        return str(ret).replace("(", "").replace(")", "").replace("'", "").replace(" ", "").replace(",", "").split(
            ";")

    def checkHostAndAddItIfNotPresent(self, host):
        values = [str(host)]
        if self.db.connection == "sqlite":
            sql = "select first_activity from Hosts WHERE mac = ? LIMIT 1"
        elif self.db.connection == "mysql":
            sql = "select first_activity from Hosts WHERE mac = %s LIMIT 1"

        ret = self.db.execquery(sql, values)
        if ret is not "" : return

        logging.info("host not registered, the host has to be added in db")

        if self.db.connection == "sqlite":
            sql = "select datetime from HTTPQueries WHERE mac_iot = ? ORDER BY datetime LIMIT 1 "
        elif self.db.connection == "mysql":
            sql = "SELECT datetime FROM HTTPQueries WHERE mac_iot = %s ORDER BY datetime LIMIT 1 "
        first_activity = self.db.execquery(sql, values)
        first_activity = str(first_activity).replace("(", "").replace(")", "").replace("'", "").replace(" ", "").replace(",", "")

        if self.db.connection == "sqlite":
            sql = "INSERT INTO Hosts (mac, hostname, first_activity) VALUES (?,?,?)"
        elif self.db.connection == "mysql":
            sql = "INSERT INTO Hosts (mac, hostname, first_activity) VALUES (%s, %s, %s)"

        values = [str(host), "", first_activity]
        self.db.execquery(sql, values)
        logging.info("Host with mac address " + host + " added in DB")


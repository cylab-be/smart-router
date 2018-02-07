#!/usr/bin/python3
import sqlite3
from datetime import datetime, timedelta
import threading
from os.path import join, dirname

import pymysql
from database import database
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
        self.learningPeriod = os.environ.get("LEARNING_PERIOD")
        self.db = database()
        self.db.connect()

    def run(self):
        logging.info("run analyser")
        macAddresses = self.getAllHosts()

        # macAddresses = ('08:00:27:54:8b:1b',':8b:1b','08:008b:1b','08:00:27:')
        # logging.debug(macAddresses)
        macAddresses = list(set(macAddresses))
        # print(macAddresses)
        for mac in macAddresses :
            # logging.debug(mac)
            self.checkHostAndAddItIfNotPresent(mac)
            self.analyse(mac)



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

        logging.info("host not registered, the host has to be added in DB.. adding it now")

        if self.db.connection == "sqlite":
            sql = "select datetime from HTTPQueries WHERE mac_iot = ? ORDER BY datetime LIMIT 1 "
        elif self.db.connection == "mysql":
            sql = "SELECT datetime FROM HTTPQueries WHERE mac_iot = %s ORDER BY datetime LIMIT 1 "
        first_activity = self.db.execquery(sql, values)
        first_activity = str(first_activity).replace("(", "").replace(")", "").replace("'", "").replace(",", "")

        if self.db.connection == "sqlite":
            sql = "INSERT INTO Hosts (mac, hostname, first_activity) VALUES (?,?,?)"
        elif self.db.connection == "mysql":
            sql = "INSERT INTO Hosts (mac, hostname, first_activity) VALUES (%s, %s, %s)"

        values = [str(host), "", first_activity]
        self.db.execquery(sql, values)
        logging.info("Host with mac address " + host + " added in DB")

    def analyse(self, host):

        if self.db.connection == "sqlite":
            sql = "SELECT first_activity FROM Hosts WHERE mac = ?"
        elif self.db.connection == "mysql":
            sql = "SELECT first_activity FROM Hosts WHERE mac = %s"
        values = [str(host)]
        firstRequestDatetime = self.db.execquery(sql, values).replace("(","").replace(")","").replace(",","").replace("'","")

        lastAllowedLearningRequestTime = datetime.strptime(firstRequestDatetime, "%Y-%m-%d %H:%M:%S.%f") + timedelta(days=int(self.learningPeriod))

        if self.db.connection == "sqlite":
            sql = "SELECT * from HTTPQueries WHERE mac_iot = ? AND domain NOT IN (SELECT domain from HTTPQueries WHERE mac_iot = ? AND datetime < ? ORDER BY datetime ) ORDER BY datetime"
        elif self.db.connection == "mysql":
            sql = "SELECT * from HTTPQueries WHERE mac_iot = %s AND domain NOT IN (SELECT domain from HTTPQueries WHERE mac_iot = %s AND datetime < %s ORDER BY datetime ) ORDER BY datetime"

        values = [str(host), str(host), str(lastAllowedLearningRequestTime)]
        maliciousDomains = self.db.execquery(sql, values)


        #FIXME - need hostname ?
        maliciousDomains = maliciousDomains.replace("(", "").replace(")", "").replace("'", "").split(";")

        for mal in maliciousDomains :
            if len(mal) > 0 :
                mal = mal.split(",")

                if self.db.connection == "sqlite":
                    sql = "SELECT * FROM Alerts WHERE mac = ? AND domain_reached = ? AND infraction_date = ?"
                elif self.db.connection == "mysql":
                    sql = "SELECT * FROM Alerts WHERE mac = %s AND domain_reached = %s AND infraction_date = %s"
                values = [str(mal[0]), str(mal[1]).replace(" ", ""), mal[2][1:]]
                ret = self.db.execquery(sql, values)
                if len(ret) > 0 : return

                if self.db.connection == "sqlite":
                    sql = "INSERT INTO Alerts (mac, domain_reached, infraction_date) VALUES (?,?,?)"
                elif self.db.connection == "mysql":
                    sql = "INSERT INTO Alerts (mac, domain_reached, infraction_date) VALUES (%s, %s, %s)"

                self.db.execquery(sql, values)




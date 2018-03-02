#!/usr/bin/python3
import sqlite3
from datetime import datetime, timedelta
import threading
from os.path import join, dirname

#import pymysql
from database import database
from dotenv import load_dotenv
from scapy.all import *
from slackclient import SlackClient


class analyser (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
#        pymysql.install_as_MySQLdb()
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        self.logfile = os.environ.get("LOGFILE")
        logging.basicConfig(filename=self.logfile, level=logging.DEBUG,format='%(asctime)s %(levelname)s - %(message)s')
        self.learningPeriod = os.environ.get("LEARNING_PERIOD")
        if "True" in os.environ.get("SLACK_NOTIFICATIONS"):
            self.slack_alert = True
        else:
            self.slack_alert = False
        self.minutes_between_analysis=os.environ.get("MINUTES_BETWEEN_ANALYSIS")

        self.slack_token = os.environ.get("SLACK_API_TOKEN")
        self.slack_channel = os.environ.get("SLACK_CHANNEL")
        self.db = database()
        self.db.connect()

    def run(self):
        self.allmaliciousdomains = []
        macAddresses = self.getAllHosts()
        macAddresses = list(set(macAddresses))
        for mac in macAddresses :
            self.checkHostAndAddItIfNotPresent(mac)
            try :
                self.allmaliciousdomains.extend(self.analyse(mac))
            except TypeError :
                # logging.warning("TYPE ERROR")
                pass
        self.allmaliciousdomains = list(filter(None, self.allmaliciousdomains))
        self.sendAlert()

    def sendAlert(self):
        if self.slack_alert is True and len(self.allmaliciousdomains) > 0 :
            sc = SlackClient(self.slack_token)
            # ret = []
            txt = "Sir, during the last " + self.minutes_between_analysis + " minutes, the next potential malicious traffic has been detected : ```"
            for row in self.allmaliciousdomains :
                txt += row.replace(", ", "->", 1).replace(',', " @", 1) + "\n"
            txt=txt[:-1]+'```'
            ret = sc.api_call(
                "chat.postMessage",
                channel=self.slack_channel,
                text=str(txt),
            )

            if ret.get('ok') is True:
                logging.info("Alert send to Slack")
            else:
                logging.error("Alert has not been send to Slack")

        else:
            logging.info("No alert sent to Slack because there is not malicious traffic detected")

    def getAllHosts(self):

        sql = "SELECT mac_iot FROM HTTPQueries"
        ret = self.db.execquery(sql)
        print ("ret : " , ret)
        return str(ret).replace("(", "").replace(")", "").replace("'", "").replace(" ", "").replace(",", "").split(
            ";")

    def checkHostAndAddItIfNotPresent(self, host):
        values = [str(host)]
        sql = "select first_activity from Hosts WHERE mac = XXX LIMIT 1"

        ret = self.db.execquery(sql, values)
        if ret is not "" : return

        logging.info("host not registered, the host has to be added in DB.. adding it now")

        sql = "SELECT datetime FROM HTTPQueries WHERE mac_iot = XXX ORDER BY datetime LIMIT 1 "
        first_activity = self.db.execquery(sql, values)
        first_activity = str(first_activity).replace("(", "").replace(")", "").replace("'", "").replace(",", "")

        sql = "INSERT INTO Hosts (mac, hostname, first_activity) VALUES (XXX, XXX, XXX)"

        values = [str(host), "", first_activity]
        self.db.execquery(sql, values)
        logging.info("Host with mac address " + host + " added in DB")

    def analyse(self, host):

        sql = "SELECT first_activity FROM Hosts WHERE mac = XXX"
        values = [str(host)]
        firstRequestDatetime = self.db.execquery(sql, values).replace("(","").replace(")","").replace(",","").replace("'","")

        lastAllowedLearningRequestTime = datetime.strptime(firstRequestDatetime, "%Y-%m-%d %H:%M:%S.%f") + timedelta(days=int(self.learningPeriod))

        sql = "SELECT * from HTTPQueries WHERE mac_iot = XXX AND domain NOT IN (SELECT domain from HTTPQueries WHERE mac_iot = XXX AND datetime < XXX ORDER BY datetime ) ORDER BY datetime"

        values = [str(host), str(host), str(lastAllowedLearningRequestTime)]
        maliciousDomains = self.db.execquery(sql, values)


        #FIXME - need hostname ?
        maliciousDomains = maliciousDomains.replace("(", "").replace(")", "").replace("'", "").split(";")

        for mal in maliciousDomains :
            if len(mal) > 0 :
                mal = mal.split(",")

                sql = "SELECT * FROM Alerts WHERE mac = XXX AND domain_reached = XXX AND infraction_date = XXX"
                values = [str(mal[0]), str(mal[1]).replace(" ", ""), mal[2][1:]]
                ret = self.db.execquery(sql, values)
                if len(ret) > 0 : return

                sql = "INSERT INTO Alerts (mac, domain_reached, infraction_date) VALUES (XXX, XXX, XXX)"

                self.db.execquery(sql, values)

        return maliciousDomains

if __name__ == "__main__":
    analyser().run()


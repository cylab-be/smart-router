#!/usr/bin/python3
import sqlite3
from datetime import datetime, timedelta
import threading
from os.path import join, dirname

#import pymysql
from dotenv import load_dotenv
from scapy.all import *
from slackclient import SlackClient
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from python.host import host
from python.httpquery import httpquery
from python.database import database
from python.alert import alert


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
        httpqueries = self.db.getAllFromTable("httpquery", "httpquery", "httpqueries")
        self.analysed_mac = []
        for query in httpqueries:
            self.checkHostAndAddItIfNotPresent(query.mac_iot)
            ret = self.analyse(query.mac_iot)
            if ret is not None :
                self.allmaliciousdomains.extend(ret)
        self.allmaliciousdomains = list(filter(None, self.allmaliciousdomains))
        self.sendAlert()

    def sendAlert(self):
        if self.slack_alert is True and len(self.allmaliciousdomains) > 0 :
            sc = SlackClient(self.slack_token)
            # ret = []
            txt = "Sir, during the last " + self.minutes_between_analysis + " minutes, the next potential malicious traffic has been detected : ```"
            for row in self.allmaliciousdomains :
                txt += str(row).replace(", ", "->", 1).replace(',', " @ ", 1) + "\n"
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

    def checkHostAndAddItIfNotPresent(self, mac_host):
        if self.db.getHostFromMac(mac_host): return

        logging.info("host not registered, the host has to be added in DB.. adding it now")
        first_activity = self.db.getDateTimeFromHttpQueryFromMacByDate(mac_host)

        #FIXME - hostname
        h = host([mac_host, 'noname.local', first_activity])
        self.db.addIntoTable("hosts", h.toTuple())

        logging.info("Host with mac address " + mac_host + " added in DB")

    def analyse(self, mac_host):

        for h in self.analysed_mac :
            if mac_host in h:
                return None
        self.analysed_mac.append(mac_host)

        first_activity = self.db.getHostFromMac(mac_host).first_activity

        last_allowed_learning_request_time = datetime.strptime(first_activity, "%Y-%m-%d %H:%M:%S.%f") + timedelta(days=int(self.learningPeriod))
        maliciousDomains = self.db.getMaliciousDomainsFromMacAfterX(mac_host, last_allowed_learning_request_time)

        for mal in maliciousDomains :
            #FIXME - fix local hostname
            a = alert([mac_host, 'noname.local', mal.domain, mal.datetime])
            self.db.insertOrIgnoreIntoTable("alerts", a.toTuple())

        return maliciousDomains

if __name__ == "__main__":
    analyser().run()


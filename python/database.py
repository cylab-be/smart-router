#!/usr/bin/python3

#import pymysql
#pymysql.install_as_MySQLdb()
#import MySQLdb
from os.path import join, dirname
from dotenv import load_dotenv
import os, sys
import logging
import sqlite3
import importlib
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from python.host import host
from python.dnsquery import dnsquery
from python.httpquery import httpquery

class database:
    def __init__(self):
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        self.logfile = os.environ.get("LOGFILE")
        logging.basicConfig(filename=self.logfile, level=logging.DEBUG, format='%(asctime)s %(levelname)s - %(message)s')
        self.connection = os.environ.get("DB_CONNECTION")
        self.dbname = os.environ.get("DB_DATABASE")

        if self.connection == 'sqlite':
            self.db_path = os.environ.get("DB_PATH")
            return
        self.host = os.environ.get("DB_HOST")
        self.port = os.environ.get("DB_PORT")
        self.user = os.environ.get("DB_USERNAME")
        self.passwd = os.environ.get("DB_PASSWORD")


    def connect(self):
        if self.connection == 'mysql':
            self.db = MySQLdb.connect(host=self.host, port=int(self.port), user=self.user, passwd=self.passwd, db=self.dbname)
        elif self.connection == 'sqlite':
            self.db = sqlite3.connect(self.dbname, check_same_thread=False)
        self.cursor = self.db.cursor()

    def execquery(self, query, *args):
        if self.connection == 'mysql':
            query = query.replace("XXX", "%s")
        elif self.connection == 'sqlite':
            query = query.replace("XXX", "?")
        try :
            #TODO test this, not sure it really works
            values = []
            for ar in args:
                values = ar
            self.cursor.execute(query, values)
            matrix =[]
            for r in self.cursor:
                matrix.append(list(r))

            self.db.commit()
            return matrix

#        except pymysql.err.ProgrammingError:
#            logging.error("SQL ERROR")
#            return False
        except sqlite3.ProgrammingError:
            logging.error("SQL ERROR")
        except sqlite3.OperationalError:
            self.createTables()
        return False

    def getAllFromTable(self, module_name, class_name, table_name):
        query = "SELECT * FROM XXX"
        #FIXME - insecure but does not work with ?
        query=query.replace("XXX", table_name)
        try:
            values = []
            self.cursor.execute(query, values)
            ret = []
            for r in self.cursor:
                #FIXME - watchout @ "python."+
                module = importlib.import_module("python."+module_name)
                class_ = getattr(module, class_name)
                instance = class_(r)
                ret.append(instance)
            self.db.commit()
            return ret

        except sqlite3.OperationalError:
            self.createTables()
            return self.getAllFromTable(module_name, class_name, table_name)

        except sqlite3.ProgrammingError:
            logging.error("SQL ERROR")
            return False

    def getHostFromMac(self, mac):
        sql = "select * from Hosts WHERE mac = XXX LIMIT 1"
        tmp = self.execquery(sql, [mac])
        if not tmp:
            return False
        return host(tmp[0])

    def getDomainFromIp(self, ip):
        sql = "select * from DNSQueries WHERE ip = XXX LIMIT 1"
        tmp = self.execquery(sql, [ip])
        if not tmp:
            return False
        return dnsquery(tmp[0]).domain

    def getDateTimeFromHttpQueryFromMacByDate(self, mac):
        sql = "SELECT * FROM HTTPQueries WHERE mac_iot = XXX ORDER BY datetime LIMIT 1 "
        tmp = self.execquery(sql, [mac])
        if not tmp:
            return False
        return httpquery(tmp[0]).datetime

    def getMaliciousDomainsFromMacAfterX(self, mac, limit_time):
        sql = "SELECT * from HTTPQueries WHERE mac_iot = XXX AND domain NOT IN (SELECT domain from HTTPQueries WHERE mac_iot = XXX AND datetime < XXX ORDER BY datetime ) ORDER BY datetime"
        sql =sql.replace("XXX", "'"+mac+"'", 2).replace("XXX", "'"+str(limit_time)+"'")
        malicious_requets = self.execquery(sql, [])
        malicious_http = []
        for mal in malicious_requets :
            malicious_http.append(httpquery(mal))
        return malicious_http


    def addIntoTable(self, table_name, insert_values):
        query = "INSERT INTO XXX VALUES XXX"

        query = query.replace("XXX", table_name, 1)
        query = query.replace("XXX", insert_values, 1)

        try:
            self.cursor.execute(query)
            self.db.commit()
            return True

        except sqlite3.ProgrammingError:
            logging.error("SQL ERROR")
            return False

    def insertOrIgnoreIntoTable(self, table_name, insert_values):
        query = "INSERT OR IGNORE INTO XXX VALUES XXX"

        query = query.replace("XXX", table_name, 1)
        query = query.replace("XXX", insert_values, 1)

        try:
            self.cursor.execute(query)
            self.db.commit()
            return True
        except sqlite3.ProgrammingError :
            logging.error("SQL ERROR")
            return False



    def createTables(self):
        fd = open(self.db_path+'create_db.sql', 'r')
        sqlFile = fd.read()
        fd.close()

        if self.connection == "sqlite":
            sqlFile  = sqlFile.replace('ENGINE=InnoDB AUTO_INCREMENT=115 DEFAULT CHARSET=latin1', '')\
                .replace('unsigned NOT NULL AUTO_INCREMENT' ,' ')

        sqlCommands = sqlFile.split(';')
        for command in sqlCommands:
            command = command.replace('\n', ' ').replace('\r', '').lstrip() + ";"
            # print(command)
            self.execquery(str(command))

        return True

    def close(self):
        self.cursor.close()
        self.db.close()

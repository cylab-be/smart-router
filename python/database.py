#!/usr/bin/python3

import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
from os.path import join, dirname
from dotenv import load_dotenv
import os
import logging
import sqlite3

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
        try :
            values = []
            for ar in args:
                values = ar
            self.cursor.execute(query, values)
            ret = ''
            for r in self.cursor:
                ret = ret + ';' + str(r)
            ret = ret[1:]
            self.db.commit()
            return str(ret)

        except pymysql.err.ProgrammingError:
            logging.error("SQL ERROR")
            return False
        except sqlite3.ProgrammingError:
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

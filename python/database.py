#!/usr/bin/python3

import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
from os.path import join, dirname
from dotenv import load_dotenv
import os

class database:
    def __init__(self):
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        self.host = os.environ.get("DB_HOST")
        self.port = os.environ.get("DB_PORT")
        self.user = os.environ.get("DB_USERNAME")
        self.passwd = os.environ.get("DB_PASSWORD")
        self.dbname = os.environ.get("DB_DATABASE")

    def connect(self):
        self.db = MySQLdb.connect(host=self.host, port=int(self.port), user=self.user, passwd=self.passwd, db=self.dbname)
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
            # TODO logging
            print("SQL ERROR")
            return False


    def close(self):
        self.cursor.close()
        self.db.close()

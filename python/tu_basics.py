import unittest
import datetime
from python.database import *


class tu_basics():
    def testCreateTables(self):
        db = database()
        db.connect()
        return database.createTables(db)

    def testTablesExistence(self):
        db = database()
        db.connect()
        sql = "SELECT * FROM DNSQueries"
        result = db.execquery(sql)
        if  result is False : return False

        sql = "SELECT * FROM HTTPQueries"
        result = db.execquery(sql)
        if result is False: return False

        return True

    def testTablesContainSomething(self):
        db = database()
        db.connect()
        sql = "SELECT * FROM DNSQueries"
        result = db.execquery(sql)
        if result is False or result is "": return False
        print("DNSQueries")
        for row in result.split(";"):
            print(row)

        sql = "SELECT * FROM HTTPQueries"
        result = db.execquery(sql)
        if result is False or result is "": return False
        print("HTTPQueries")
        for row in result.split(";"):
            print(row)
        return True


    def testInserIntoTables(self):
        db = database()
        db.connect()
        now = datetime.datetime.now()
        values = [str("1.1.1.1"), str("2.2.2.2"), str("test.org"), now]
        if db.connection == "sqlite":
            sql = "INSERT INTO DNSQueries (ip_iot, ip_dst, domain, datetime) VALUES (?,?,?,?)"
        elif db.connection == "mysql":
            sql = "INSERT INTO DNSQueries (ip_iot, ip_dst, domain, datetime) VALUES (%s, %s, %s, %s)"
        if db.execquery(sql, values) == False: return False

        values = [str("1.1.1.1"), str("test.org"), now]
        if db.connection == "sqlite":
            sql = "INSERT INTO HTTPQueries (ip_iot, domain, datetime) VALUES (?,?,?)"
        elif db.connection == "mysql":
            sql = "INSERT INTO HTTPQueries (ip_iot, domain, datetime) VALUES (%s, %s, %s)"
        if db.execquery(sql, values) == False: return False

        return True

    def testTableDNSQueriesContains(self):
        db = database()
        db.connect()
        sql = "SELECT * FROM DNSQueries"
        return db.execquery(sql)

    def testTableHTTPQueriesContains(self):
        db = database()
        db.connect()
        sql = "SELECT * FROM HTTPQueries"
        return db.execquery(sql)


class ExecuteSniffTests(unittest.TestCase):
    def testCreateTables(self):
        self.assertTrue(tu_basics.testCreateTables(self), "Tables can not been created")
    def testInserIntoTables(self):
        self.assertTrue(tu_basics.testInserIntoTables(self), "Insertion in tables failed")
    def testTablesExistence(self):
        self.assertTrue(tu_basics.testTablesExistence(self), "Tables do not exist")
    def testTableDNSQueriesContains(self):
        self.assertTrue(tu_basics.testTableDNSQueriesContains(self), "Insertion in DNSQueries table must have been fail because there is nothing in there")
    def testTableHTTPQueriesContains(self):
        self.assertTrue(tu_basics.testTableHTTPQueriesContains(self), "Insertion in HTTPQueries table must have been fail because there is nothing in there")

import unittest
import datetime
from python.database import *


class SniffTests():
    def testCreateTables(self):
        db = database()
        db.connect()
        return database.createTables(db)

    def testTablesExistence(self):
        db = database()
        db.connect()
        sql = "SELECT * FROM DNSQueries"
        result = db.execquery(sql)
        if  result == False : return False
        print("DNSQueries")
        for row in result.split(";") :
            print(row)

        sql = "SELECT * FROM HTTPQueries"
        result = db.execquery(sql)
        if result == False: return False
        print("HTTPQueries")
        for row in result.split(";") :
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
        self.assertTrue(SniffTests.testCreateTables(self), "Tables can not been created")
    def testTablesExistence(self):
        self.assertTrue(SniffTests.testTablesExistence(self), "Tables do not exist")
    def testInserIntoTables(self):
        self.assertTrue(SniffTests.testInserIntoTables(self), "Insertion in tables failed")
    def testTableDNSQueriesContains(self):
        self.assertTrue(SniffTests.testTableDNSQueriesContains(self), "Insertion in DNSQueries table must have been fail because there is nothing in there")
    def testTableHTTPQueriesContains(self):
        self.assertTrue(SniffTests.testTableHTTPQueriesContains(self), "Insertion in HTTPQueries table must have been fail because there is nothing in there")

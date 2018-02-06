import unittest
from datetime import datetime, timedelta
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

        sql = "SELECT * FROM Hosts"
        result = db.execquery(sql)
        if result is False: return False

        sql = "SELECT * FROM Alerts"
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

        sql = "SELECT * FROM Hosts"
        result = db.execquery(sql)
        if result is False or result is "": return False
        print("Hosts")
        for row in result.split(";"):
            print(row)

        sql = "SELECT * FROM Alerts"
        result = db.execquery(sql)
        if result is False or result is "": return False
        print("Alerts")
        for row in result.split(";"):
            print(row)
        return True


    def testInserIntoTables(self):
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        self.learningPeriod = os.environ.get("LEARNING_PERIOD")

        db = database()
        db.connect()
        now = datetime.now()
        values = [str("2.2.2.2"), str("test.org"), now]
        if db.connection == "sqlite":
            sql = "INSERT INTO DNSQueries (ip , domain, datetime) VALUES (?,?,?)"
        elif db.connection == "mysql":
            sql = "INSERT INTO DNSQueries (ip, domain, datetime) VALUES (%s, %s, %s)"
        if db.execquery(sql, values) == False: return False

        values = [str("aa:bb:cc:dd:ee:ff"), str("malicious.org"), now]
        if db.connection == "sqlite":
            sql = "INSERT INTO HTTPQueries (mac_iot, domain, datetime) VALUES (?,?,?)"
        elif db.connection == "mysql":
            sql = "INSERT INTO HTTPQueries (mac_iot, domain, datetime) VALUES (%s, %s, %s)"
        if db.execquery(sql, values) == False: return False

        values = [str("aa:bb:cc:dd:ee:ff"), str("iot.local"), now]
        if db.connection == "sqlite":
            sql = "INSERT INTO Hosts (mac, hostname, first_activity) VALUES (?,?,?)"
        elif db.connection == "mysql":
            sql = "INSERT INTO Hosts (mac, hostname, first_activity) VALUES (%s, %s, %s)"
        if db.execquery(sql, values) == False: return False


        values = [str("aa:bb:cc:dd:ee:ff"), str("iot.local"), str("test.org"), now]
        if db.connection == "sqlite":
            sql = "INSERT INTO Alerts (mac, hostname, domain_reached, infraction_date) VALUES (?,?,?,?)"
        elif db.connection == "mysql":
            sql = "INSERT INTO Alerts (mac, hostname, domain_reached, infraction_date) VALUES (%s, %s, %s, %s)"
        if db.execquery(sql, values) == False: return False

        return True

    def testInserIntoTablesForAnalysisSimulation(self):
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        self.learningPeriod = os.environ.get("LEARNING_PERIOD")

        db = database()
        db.connect()
        now = datetime.now()
        values = [str("2.2.2.2"), str("test.org"), now]
        if db.connection == "sqlite":
            sql = "INSERT INTO DNSQueries (ip , domain, datetime) VALUES (?,?,?)"
        elif db.connection == "mysql":
            sql = "INSERT INTO DNSQueries (ip, domain, datetime) VALUES (%s, %s, %s)"
        if db.execquery(sql, values) == False: return False

        values = [str("aa:bb:cc:dd:ee:ff"), str("malicious.org"), now]
        if db.connection == "sqlite":
            sql = "INSERT INTO HTTPQueries (mac_iot, domain, datetime) VALUES (?,?,?)"
        elif db.connection == "mysql":
            sql = "INSERT INTO HTTPQueries (mac_iot, domain, datetime) VALUES (%s, %s, %s)"
        if db.execquery(sql, values) == False: return False
        values = [str("aa:bb:cc:dd:ee:ff"), str("legit.org"), str(now - timedelta(days=int(self.learningPeriod) + 1))]
        if db.execquery(sql, values) == False: return False
        values = [str("aa:bb:cc:dd:ee:ff"), str("legit2.org"), str(now - timedelta(days=int(self.learningPeriod) + 3) + timedelta(seconds=5))]
        if db.execquery(sql, values) == False: return False

        values = [str("11:22:33:44:55:66"), str("legit.org"), str(now - timedelta(days=int(self.learningPeriod) + 2))]
        if db.execquery(sql, values) == False: return False
        values = [str("11:22:33:44:55:66"), str("legit2.org"), str(now - timedelta(days=int(self.learningPeriod) + 4) + timedelta(seconds=5))]
        if db.execquery(sql, values) == False: return False
        values = [str("11:22:33:44:55:66"), str("malicious.org"), str(now)]
        if db.execquery(sql, values) == False: return False
        values = [str("11:22:33:44:55:66"), str("malicious2.org"), str(now + timedelta(seconds=5))]
        if db.execquery(sql, values) == False: return False
        values = [str("11:22:33:AA:BB:CC"), str("legit3.org"), str(now - timedelta(days=int(self.learningPeriod) - 5) - timedelta(seconds=5))]
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

    def testTableHostsContains(self):
        db = database()
        db.connect()
        sql = "SELECT * FROM Hosts"
        return db.execquery(sql)

    def testTableAlertsContains(self):
        db = database()
        db.connect()
        sql = "SELECT * FROM Alerts"
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
    def testTableHostsContains(self):
        self.assertTrue(tu_basics.testTableHostsContains(self), "Insertion in Hosts table must have been fail because there is nothing in there")
    def testTableAlertsContains(self):
        self.assertTrue(tu_basics.testTableAlertsContains(self), "Insertion in Alerts table must have been fail because there is nothing in there")

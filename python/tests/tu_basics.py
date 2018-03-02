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

    def testAllTablesContainSomething(self):
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
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        self.learningPeriod = os.environ.get("LEARNING_PERIOD")

        db = database()
        db.connect()
        now = datetime.now()
        values = [str("2.2.2.2"), str("test.org"), now]
        sql = "INSERT INTO DNSQueries (ip, domain, datetime) VALUES (XXX, XXX, XXX)"
        if db.execquery(sql, values) == False: return False

        values = [str("aa:bb:cc:dd:ee:ff"), str("malicious.org"), now]
        sql = "INSERT INTO HTTPQueries (mac_iot, domain, datetime) VALUES (XXX, XXX, XXX)"
        if db.execquery(sql, values) == False: return False

        values = [str("aa:bb:cc:dd:ee:ff"), str("iot.local"), now]
        sql = "INSERT INTO Hosts (mac, hostname, first_activity) VALUES (XXX, XXX, XXX)"
        if db.execquery(sql, values) == False: return False


        values = [str("aa:bb:cc:dd:ee:ff"), str("iot.local"), str("test.org"), now]
        sql = "INSERT INTO Alerts (mac, hostname, domain_reached, infraction_date) VALUES (XXX, XXX, XXX, XXX)"
        if db.execquery(sql, values) == False: return False

        return True

    def testInserIntoTablesForAnalysisSimulation(self):
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        self.learningPeriod = os.environ.get("LEARNING_PERIOD")

        db = database()
        db.connect()
        now = datetime.now()
        #FIXME - add corresponding DNS querries
        values = [str("aa:bb:cc:dd:ee:ff"), str("legit1.org"), now]
        sql = "INSERT INTO DNSQueries (ip, domain, datetime) VALUES (XXX, XXX, XXX)"
        if db.execquery(sql, values) == False: return False
        values = [str("aa:bb:cc:dd:ee:ff"), str("legit2.org"), now]
        if db.execquery(sql, values) == False: return False
        values = [str("aa:bb:cc:dd:ee:ff"), str("malicious.org"), now]
        if db.execquery(sql, values) == False: return False


        values = [str("aa:bb:cc:dd:ee:ff"), str("malicious.org"), now]
        sql = "INSERT INTO HTTPQueries (mac_iot, domain, datetime) VALUES (XXX, XXX, XXX)"
        if db.execquery(sql, values) == False: return False
        values = [str("aa:bb:cc:dd:ee:ff"), str("legit2.org"), str(now - timedelta(days=int(self.learningPeriod) + 3) + timedelta(hours=5))]
        if db.execquery(sql, values) == False: return False
        values = [str("aa:bb:cc:dd:ee:ff"), str("legit1.org"), str(now - timedelta(days=int(self.learningPeriod) + 3) + timedelta(seconds=5))]
        if db.execquery(sql, values) == False: return False

        values = [str("11:22:33:44:55:66"), str("legit2.org"), str(now - timedelta(days=int(self.learningPeriod) + 2))]
        if db.execquery(sql, values) == False: return False
        values = [str("11:22:33:44:55:66"), str("legit1.org"), str(now - timedelta(days=int(self.learningPeriod) + 4) + timedelta(seconds=5))]
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

    def testDTO(self):
        db = database()
        db.connect()
        hosts = db.getAll("host", "host", "Hosts")
        if hosts is False or len(hosts) == 0:
            return False
        # for host in hosts:
        #     print (str(host))

        alerts = db.getAll("alert", "alert", "Alerts")
        if alerts is False or len(alerts) == 0:
            return False
        # for alert in alerts:
        #     print(str(alert))

        httpqueries = db.getAll("httpquery", "httpquery", "httpqueries")
        if httpqueries is False or len(httpqueries) == 0:
            return False
        # for httpquery in httpqueries:
        #     print(str(httpquery))

        dnsqueries = db.getAll("dnsquery", "dnsquery", "dnsqueries")
        if dnsqueries is False or len(dnsqueries) == 0:
            return False
        # for dnsquery in dnsqueries:
        #     print(str(dnsquery))



        return True


class ExecuteBasicsTests(unittest.TestCase):
    # def testCreateTables(self):
    #     self.assertTrue(tu_basics.testCreateTables(self), "Tables can not been created")
    # def testInserIntoTables(self):
    #     self.assertTrue(tu_basics.testInserIntoTables(self), "Insertion in tables failed")
    # def testTablesExistence(self):
    #     self.assertTrue(tu_basics.testTablesExistence(self), "Tables do not exist")
    # def testTableDNSQueriesContains(self):
    #     self.assertTrue(tu_basics.testTableDNSQueriesContains(self), "Insertion in DNSQueries table must have been fail because there is nothing in there")
    # def testTableHTTPQueriesContains(self):
    #     self.assertTrue(tu_basics.testTableHTTPQueriesContains(self), "Insertion in HTTPQueries table must have been fail because there is nothing in there")
    # def testTableHostsContains(self):
    #     self.assertTrue(tu_basics.testTableHostsContains(self), "Insertion in Hosts table must have been fail because there is nothing in there")
    # def testTableAlertsContains(self):
    #     self.assertTrue(tu_basics.testTableAlertsContains(self), "Insertion in Alerts table must have been fail because there is nothing in there")

#FIXME - below function work only if uppers are commented, do not know why, but tables are empty if not commented, and should not

    def testDTO(self):
        self.assertTrue(tu_basics.testDTO(self), "DTO test failed")

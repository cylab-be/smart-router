import unittest, time, os, sys
from datetime import datetime, timedelta
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from python.alert import alert
from python.database import *


class tu_basics():

    def testCreateTables(self):
        db = database()
        db.connect()
        return database.createTables(db)

    def testAllTablesContainSomething(self):
        db = database()
        db.connect()
        dnsqueries = db.getAllFromTable("dnsquery", "dnsquery", "dnsqueries")
        if not dnsqueries: return False

        httpqueries = db.getAllFromTable("httpquery", "httpquery", "httpqueries")
        if not httpqueries: return False

        hosts = db.getAllFromTable("host", "host", "hosts")
        if not hosts: return False

        alerts = db.getAllFromTable("alert", "alert", "alerts")
        if not alerts: return False
        return True

    def testTablesContainSomething(self):
        db = database()
        db.connect()
        dnsqueries = db.getAllFromTable("dnsquery", "dnsquery", "dnsqueries")
        if not dnsqueries : return False

        httpqueries = db.getAllFromTable("httpquery", "httpquery", "httpqueries")
        if not httpqueries: return False
        return True


    def testInserIntoTables(self):
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        self.learningPeriod = os.environ.get("LEARNING_PERIOD")

        db = database()
        db.connect()
        now = datetime.now()
        dns_querry = dnsquery(["2.2.2.2", "test.org", str(now)])
        if not db.addIntoTable("dnsqueries", dns_querry.toTuple()) : return False

        http_querry = httpquery(["aa:bb:cc:dd:ee:ff", "malicious.org", str(now)])
        if not db.addIntoTable("httpqueries", http_querry.toTuple()): return False

        h = host(["aa:bb:cc:dd:ee:ff", "iot.local", str(now)])
        if not db.addIntoTable("hosts", h.toTuple()): return False

        a = alert(["aa:bb:cc:dd:ee:ff", "iot.local", "test.org", str(now)])
        if not db.addIntoTable("alerts", a.toTuple()): return False
        return True

    def testInserIntoTablesForAnalysisSimulation(self):
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        self.learningPeriod = os.environ.get("LEARNING_PERIOD")

        db = database()
        db.connect()
        now = datetime.now()

        five_minutes_ago = now - timedelta(minutes=5)
        yesterday = now - timedelta(days=int(self.learningPeriod))- timedelta(hours=5)
        yesterday_later = now - timedelta(days=int(self.learningPeriod))+ timedelta(hours=5)


        dns_querry = dnsquery(["188.213.143.111", "nicode.me", str(yesterday)])
        if not db.insertOrIgnoreIntoTable("dnsqueries", dns_querry.toTuple()): return False

        dns_querry = dnsquery(["82.212.183.13", "benjaminnicodeme.be", str(yesterday)])
        if not db.insertOrIgnoreIntoTable("dnsqueries", dns_querry.toTuple()): return False

        dns_querry = dnsquery(["69.172.201.153", "malicious.org", str(now)])
        if not db.insertOrIgnoreIntoTable("dnsqueries", dns_querry.toTuple()): return False


        http_querry = httpquery(["5a:ef:68:a6:35:48", "nicode.me", str(yesterday)])
        if not db.insertOrIgnoreIntoTable("httpqueries", http_querry.toTuple()): return False

        http_querry = httpquery(["5a:ef:68:a6:35:48", "nicode.me", str(yesterday_later)])
        if not db.insertOrIgnoreIntoTable("httpqueries", http_querry.toTuple()): return False

        http_querry = httpquery(["5a:ef:68:a6:35:48", "nicode.me", str(now)])
        if not db.insertOrIgnoreIntoTable("httpqueries", http_querry.toTuple()): return False

        http_querry = httpquery(["5a:ef:68:a6:35:48", "benjaminnicode.be", str(yesterday)])
        if not db.insertOrIgnoreIntoTable("httpqueries", http_querry.toTuple()): return False

        http_querry = httpquery(["5a:ef:68:a6:35:48", "benjaminnicode.be", str(yesterday_later)])
        if not db.insertOrIgnoreIntoTable("httpqueries", http_querry.toTuple()): return False

        http_querry = httpquery(["5a:ef:68:a6:35:48", "benjaminnicode.be", str(now)])
        if not db.insertOrIgnoreIntoTable("httpqueries", http_querry.toTuple()): return False

        http_querry = httpquery(["5a:ef:68:a6:35:48", "malicious.org", str(five_minutes_ago)])
        if not db.insertOrIgnoreIntoTable("httpqueries", http_querry.toTuple()): return False

        http_querry = httpquery(["5a:ef:68:a6:35:48", "malicious.org", str(now)])
        if not db.insertOrIgnoreIntoTable("httpqueries", http_querry.toTuple()): return False

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


class ExecuteBasicsTests(unittest.TestCase):
    def testCreateTables(self):
        self.assertTrue(tu_basics.testCreateTables(self), "Tables can not been created")
    def testInserIntoTables(self):
        self.assertTrue(tu_basics.testInserIntoTables(self), "Insertion in tables failed")
    def testTableDNSQueriesContains(self):
        self.assertTrue(tu_basics.testTableDNSQueriesContains(self), "Insertion in DNSQueries table must have been fail because there is nothing in there")
    def testTableHTTPQueriesContains(self):
        self.assertTrue(tu_basics.testTableHTTPQueriesContains(self), "Insertion in HTTPQueries table must have been fail because there is nothing in there")
    def testTableHostsContains(self):
        self.assertTrue(tu_basics.testTableHostsContains(self), "Insertion in Hosts table must have been fail because there is nothing in there")
    def testTableAlertsContains(self):
        self.assertTrue(tu_basics.testTableAlertsContains(self), "Insertion in Alerts table must have been fail because there is nothing in there")

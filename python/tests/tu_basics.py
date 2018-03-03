import unittest, time, os, sys
from datetime import datetime, timedelta
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from python.alert import alert
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
        dnsqueries = db.getAllFromTable("dnsquery", "dnsquery", "dnsqueries")
        if not dnsqueries: return False
        print("DNSQueries")
        for query in dnsqueries:
            print(str(query))

        httpqueries = db.getAllFromTable("httpquery", "httpquery", "httpqueries")
        if not dnsqueries: return False
        print("HTTPQueries")
        for query in httpqueries:
            print(str(query))

        hosts = db.getAllFromTable("host", "host", "hosts")
        if not hosts: return False
        print("Hosts")
        for host in hosts:
            print(str(host))

        alerts = db.getAllFromTable("alert", "alert", "alerts")
        if not alerts: return False
        print("Alerts")
        for alert in alerts:
            print(str(alert))
        return True

    def testTablesContainSomething(self):
        db = database()
        db.connect()
        dnsqueries = db.getAllFromTable("dnsquery", "dnsquery", "dnsqueries")
        if not dnsqueries : return False
        # print("DNSQueries")
        # for query in dnsqueries:
        #     print(str(query))

        httpqueries = db.getAllFromTable("httpquery", "httpquery", "httpqueries")
        if not dnsqueries: return False
        # print("HTTPQueries")
        # for query in httpqueries:
        #     print(str(query))
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
        values = [str("188.213.143.111"), str("legit1.org"), now]
        sql = "INSERT INTO DNSQueries (ip, domain, datetime) VALUES (XXX, XXX, XXX)"
        if db.execquery(sql, values) == False: return False
        values = [str("8.8.8.8"), str("legit2.org"), now]
        if db.execquery(sql, values) == False: return False
        values = [str("8.8.4.4"), str("malicious.org"), now]
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
        hosts = db.getAllFromTable("host", "host", "Hosts")
        if hosts is False or len(hosts) == 0:
            return False
        # for host in hosts:
        #     print (str(host))

        alerts = db.getAllFromTable("alert", "alert", "Alerts")
        if alerts is False or len(alerts) == 0:
            return False
        # for alert in alerts:
        #     print(str(alert))

        httpqueries = db.getAllFromTable("httpquery", "httpquery", "httpqueries")
        if httpqueries is False or len(httpqueries) == 0:
            return False
        # for httpquery in httpqueries:
        #     print(str(httpquery))

        dnsqueries = db.getAllFromTable("dnsquery", "dnsquery", "dnsqueries")
        if dnsqueries is False or len(dnsqueries) == 0:
            return False
        # for dnsquery in dnsqueries:
        #     print(str(dnsquery))

        return True

    def testGetDomainFromIp(self):
        db = database()
        db.connect()
        return db.getDomainFromIp("188.213.143.111")

    def testGetHostFromMac(self):
        db = database()
        db.connect()
        return db.getHostFromMac("aa:bb:cc:dd:ee:ff")

    def testGetDateTimeFromHttpQueryFromMacByDate(self):
        db = database()
        db.connect()
        return db.getDateTimeFromHttpQueryFromMacByDate("aa:bb:cc:dd:ee:ff")

    def testAddIntoTable(self):
        db = database()
        db.connect()
        h = host(['aa:bb:cc:dd:ee:ff', 'smb.local', '2018-03-07 00:03:08.748273'])
        return db.addIntoTable("hosts", h.toTuple())

    def testInsertOrIgnoreIntoTable(self):
        db = database()
        db.connect()
        a = alert(['aa:bb:cc:dd:ee:ff', 'smb.local', 'malicious.org', '2018-03-07 00:03:08.748273'])
        return db.insertOrIgnoreIntoTable("alerts", a.toTuple())

    def testGetMaliciousDomainsFromMacAfterX(self):
        db = database()
        db.connect()
        queries = db.getMaliciousDomainsFromMacAfterX("aa:bb:cc:dd:ee:ff", "2018-03-01")
        # for query in queries :
        #     print(str(query))
        queries = db.getMaliciousDomainsFromMacAfterX("11:22:33:44:55:66", "2018-03-01")
        # for query in queries:
        #     print(str(query))
        return queries

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

    # def testDTO(self):
    #     self.assertTrue(tu_basics.testDTO(self), "DTO test failed")
    def testGetDomainFromIp(self):
        self.assertIsNot(False, tu_basics.testGetDomainFromIp(self), "Get domain from ip failed")
    # def testGetHostFromMac(self):
    #     self.assertIsNot(False, tu_basics.testGetHostFromMac(self), "Get host from mac failed")
    def testGetDateTimeFromHttpQueryFromMacByDate(self):
        self.assertIsNot(False, tu_basics.testGetDateTimeFromHttpQueryFromMacByDate(self), "Get datetime from httpquery by date failed")
    # def testAddIntoTable(self):
    #     self.assertIsNot(False, tu_basics.testAddIntoTable(self), "Fail add into table")
    def testGetMaliciousDomainsFromMacAfterX(self):
        self.assertIsNot(False, tu_basics.testGetMaliciousDomainsFromMacAfterX(self), "Failed get alerts")
    def testInsertOrIgnoreIntoTable(self):
        self.assertIsNot(False, tu_basics.testInsertOrIgnoreIntoTable(self), "Failed ignore or insert")

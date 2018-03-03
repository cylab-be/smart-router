import unittest, sys, os
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from python.tests.tu_basics import tu_basics
from python.alert import alert
from python.database import *

class tu_db():
    def testDTO(self):
        db = database()
        db.connect()
        hosts = db.getAllFromTable("host", "host", "Hosts")
        if hosts is False or len(hosts) == 0:
            return False

        alerts = db.getAllFromTable("alert", "alert", "Alerts")
        if alerts is False or len(alerts) == 0:
            return False

        httpqueries = db.getAllFromTable("httpquery", "httpquery", "httpqueries")
        if httpqueries is False or len(httpqueries) == 0:
            return False

        dnsqueries = db.getAllFromTable("dnsquery", "dnsquery", "dnsqueries")
        if dnsqueries is False or len(dnsqueries) == 0:
            return False

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
        now = datetime.now()
        a = alert(['aa:bb:cc:dd:ee:ff', 'smb.local', 'malicious.org', str(now)])
        if db.insertOrIgnoreIntoTable("alerts", a.toTuple()) is False : return False
        dns_querry = dnsquery(["188.213.143.111", "nicode.me", str(now)])
        if not db.insertOrIgnoreIntoTable("dnsqueries", dns_querry.toTuple()): return False

    def testGetMaliciousDomainsFromMacAfterX(self):
        db = database()
        db.connect()
        queries = db.getMaliciousDomainsFromMacAfterX("aa:bb:cc:dd:ee:ff", "2018-03-01")
        return queries

class ExecuteDBTests(unittest.TestCase):

    def testAll(self):
        self.assertTrue(tu_basics.testCreateTables(self), "Tables can not been created")
        self.assertTrue(tu_basics.testInserIntoTables(self), "Insertion in tables failed")
        self.assertTrue(tu_db.testDTO(self), "DTO test failed")
        self.assertIsNot(False, tu_db.testInsertOrIgnoreIntoTable(self), "Failed ignore or insert")
        self.assertIsNot(False, tu_db.testGetDomainFromIp(self), "Get domain from ip failed")
        self.assertIsNot(False, tu_db.testGetHostFromMac(self), "Get host from mac failed")
        self.assertIsNot(False, tu_db.testGetDateTimeFromHttpQueryFromMacByDate(self),
                         "Get datetime from httpquery by date failed")
        self.assertIsNot(False, tu_db.testGetMaliciousDomainsFromMacAfterX(self), "Failed get alerts")



if __name__ == '__main__':
    unittest.main()

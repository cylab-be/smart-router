import unittest
import multiprocessing
import requests
from sniffer import sniffer
from tu_basics import tu_basics


class tu_allsnifferprocess():
    def testAllSniffer(self):
        p = multiprocessing.Process(target=snif)
        p.start()
        p.join(5)
        r = requests.get("http://nicode.me/index.html")
        # Wait for 10 seconds or until process finishes
        p.join(10)
        # If thread is still active
        if p.is_alive():
            print("running... let s kill it...")
            # Terminate
            p.terminate()
            p.join()


class Executetu_allsnifferprocess(unittest.TestCase):
    def testSniffing(self):
        self.assertTrue(tu_basics.testCreateTables(self), "Tables can not been created")
        self.assertTrue(tu_basics.testTablesExistence(self), "Tables do not exist")
        tu_allsnifferprocess.testAllSniffer(self)
        self.assertTrue(tu_basics.testTablesContainSomething(self), "Tables do not contain anything")


def snif():
    snifDNS = sniffer("dns")
    snifDNS.setHost("10.0.2.15")
    snifDNS.start()

    snifHTTP = sniffer("http")
    snifHTTP.setHost("10.0.2.15")
    snifHTTP.start()

    snifDNS.join()
    snifHTTP.join()

if __name__ == '__main__':
    unittest.main()

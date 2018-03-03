import unittest, time, os, sys
import multiprocessing
import requests
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from python.sniffer import sniffer
from python.analyser import analyser
from python.tests.tu_basics import tu_basics



def snif():
    snifDNS = sniffer("dns")
    snifDNS.setHost("")
    snifDNS.start()

    snifHTTP = sniffer("http")
    snifHTTP.setHost("")
    snifHTTP.start()

    snifHTTPS = sniffer("https")
    snifHTTPS.setHost("")
    snifHTTPS.start()

    snifDNS.join()
    snifHTTP.join()
    snifHTTPS.join()

def analyse():
    a = analyser()
    a.start()
    a.join()

class tu_allprocess():
    def testSniffer(self):
        p = multiprocessing.Process(target=snif)
        p.start()
        # p.join(5)
        p.join(5)
        r = requests.get("http://nicode.me/index.html")
        # Wait for 10 seconds or until process finishes
        # p.join(10)
        p.join(10)
        # If thread is still active
        if p.is_alive():
            print("running... let s kill it...")
            # Terminate
            p.terminate()
            p.join()

    def testAnalyser(self):
        p = multiprocessing.Process(target=analyse)
        p.start()
        p.join(10)


class Executetu_allprocess(unittest.TestCase):

    # def testSniffer(self):
    #     self.assertTrue(tu_basics.testCreateTables(self), "Tables can not been created")
    #     tu_allprocess.testSniffer(self)
    #     self.assertTrue(tu_basics.testTablesContainSomething(self), "Tables do not contain anything after sniffing")

    def testAnalyser(self):
        self.assertTrue(tu_basics.testCreateTables(self), "Tables can not been created")
        self.assertTrue(tu_basics.testInserIntoTablesForAnalysisSimulation(self), "Can not create insert into tables")
        self.assertTrue(tu_basics.testTablesContainSomething(self), "Tables do not contain anything after inserting")

        tu_allprocess.testAnalyser(self)
        self.assertTrue(tu_basics.testAllTablesContainSomething(self), "Tables do not contain anything after analysing")


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/python3
import datetime
import threading
from os.path import join, dirname
from python.database import database
from dotenv import load_dotenv
from scapy.all import *
from scapy.layers.dns import DNS, DNSRR
from scapy.layers.inet import IP
from scapy.layers.inet import Ether
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
#import pymysql
from python.httpquery import httpquery
from python.dnsquery import dnsquery


class sniffer (threading.Thread):

    def __init__(self, type):
        threading.Thread.__init__(self)
        #pymysql.install_as_MySQLdb()
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        self.logfile = os.environ.get("LOGFILE")
        logging.basicConfig(filename=self.logfile, level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s - %(message)s')
        self.interface = os.environ.get("INTERFACE")
        self.db = database()
        self.db.connect()
        self.type = type

    def run(self):
        logging.info("Starting " + self.type +" sniffer")
        if (self.type == "dns"):
            self.dnsQuerry()
        elif (self.type == "http"):
            self.httpQuerry()
        elif (self.type == "https"):
            self.httpsQuerry()

    def dnsQuerryHandler(self, pkt):
        if IP not in pkt: return
        if not pkt.haslayer(DNS): return
        if not pkt.ancount > 0 and not isinstance(pkt.an, DNSRR): return
        dest = pkt.an.rdata
        domain = str(pkt.getlayer(DNS).qd.qname.decode("utf-8"))
        if domain.endswith('.'):
            domain = domain[:-1]

        socket.inet_aton(dest)
        now = datetime.datetime.now()
        dns_querry = httpquery([dest, domain, str(now)])
        #Add domain only if ipx domain not present in dns querry table, can be changed by using addTable() function
        if self.db.insertOrIgnoreIntoTable("dnsqueries", dns_querry.toTuple()):
            logging.info("new entry in database(DNS) : " + domain)
        else:
            logging.error("failed inserting DNS tuple in database")

    def httpQuerryHandler(self, pkt):
        #FIXME - redo with correct db logic
        if IP not in pkt: return
        ip_dst = pkt[IP].dst
        ip_src = pkt[IP].src

        if not pkt['TCP'].flags & 2: return

        # FIXME - Tghe first time tho domain is reached, it is add to DNS tables, beacause of this addition, first request to DNS table can return False if DB is to "slow" to add the DNS entry and commit it
        # time.sleep(2)
        domain = self.db.getDomainFromIp(str(ip_dst))

        if domain :
            ip = str(pkt[Ether].dst)
        else:
            domain = self.db.getDomainFromIp(str(ip_src))
            if not domain :
                #Using ip dst if no domains availmables to not lose data
                logging.warning("No corresponding domain, using "+ip_dst+" instead")
                # return False
                domain = ip_dst
            ip = str(pkt[Ether].src)

        now = datetime.datetime.now()

        http_querry = httpquery([ip, domain, str(now)])
        if not self.db.insertOrIgnoreIntoTable("httpqueries", http_querry.toTuple()):
            logging.error("failed inserting HTTP tuple in database")
        else:
            logging.info("new entry in database(HTTP(s)) : " + domain)



    def dnsQuerry(self):
        # TODO - check if host, if not, launch sniff wo filter on ip add
        # sniff(iface=self.interface, filter="ip host " + host + " and port 53", prn=self.dnsQuerryHandler, store=0)
        sniff(iface=self.interface, filter="port 53", prn=self.dnsQuerryHandler, store=0)

    def httpQuerry(self):
        # TODO - check if host, if not, launch sniff wo filter on ip add
        # sniff(iface=self.interface, filter="ip host " + host + " and port 80", prn=self.httpQuerryHandler, store=0)
        # sniff(iface=self.interface, filter="port 80", lfilter=lambda d: d.src == '08:00:27:54:8b:1b', prn=self.httpQuerryHandler, store=0)
        sniff(iface=self.interface, filter="port 80", prn=self.httpQuerryHandler, store=0)

    def httpsQuerry(self):
        # TODO - check if host, if not, launch sniff wo filter on ip add
        sniff(iface=self.interface, filter="port 443", prn=self.httpQuerryHandler, store=0)

#!/usr/bin/python3
import datetime
import threading
from os.path import join, dirname

#import pymysql
from database import database
from dotenv import load_dotenv
from scapy.all import *
from scapy.layers.dns import DNS, DNSRR
from scapy.layers.inet import IP
from scapy.layers.inet import Ether
from host import host
from dnsquery import dnsquery


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
        self.host = ""

    def run(self):
        logging.info("run " + self.type)
        if (self.type == "dns"):
            self.dnsQuerry(self.host)
        elif (self.type == "http"):
            self.httpQuerry(self.host)
        elif (self.type == "https"):
            self.httpsQuerry(self.host)

    def setHost(self, host):
        self.host = host

    def dnsQuerryHandler(self, pkt):
        if IP not in pkt: return
        if not pkt.haslayer(DNS): return
        if not pkt.ancount > 0 and not isinstance(pkt.an, DNSRR): return
        dest = pkt.an.rdata
        name = str(pkt.getlayer(DNS).qd.qname.decode("utf-8"))
        if name.endswith('.'):
            name = name[:-1]
        try:
            socket.inet_aton(dest)
            now = datetime.datetime.now()
            values = [str(dest), str(name), now]
            sql = "INSERT INTO DNSQueries (ip, domain, datetime) VALUES (XXX,XXX,XXX)"
            if self.db.execquery(sql, values):
                logging.error("failed inserting tuple in database")
            else:
                logging.info("new entry in database(DNS)")
        except socket.error: pass
        except TypeError: pass

    def httpQuerryHandler(self, pkt):
        if IP not in pkt: return
        ip_dst = pkt[IP].dst
        ip_src = pkt[IP].src

        values = [str(ip_dst)]

        if not pkt['TCP'].flags & 2: return

        # FIXME - dns request in db "fail" for the first time the domain is reached, so the first http request also fail
        time.sleep(2)

        sql = "select * from DNSQueries WHERE ip = XXX LIMIT 1"
        tmp = self.db.execquery(sql, values)

        if tmp :
            ret_dnsquery = dnsquery(tmp[0])
            ip = str(pkt[Ether].dst)
        else:
            values = [str(ip_src)]
            tmp = self.db.execquery(sql, values)
            if not tmp :
                logging.warning("No corresponding domain")
                return False
            ret_dnsquery = dnsquery(tmp[0])
            ip = str(pkt[Ether].src)

        print(str(ret_dnsquery))

        domain = ret_dnsquery.domain
        now = datetime.datetime.now()
        sql = "INSERT INTO HTTPQueries (mac_iot, domain, datetime) VALUES (XXX,XXX,XXX)"

        values = [ip, str(domain), now]

        if self.db.execquery(sql, values):
            logging.error("failed inserting tuple in database")
        else:
            logging.info("new entry in database(HTTP)")



    def dnsQuerry(self, host):
        # TODO - check if host, if not, launch sniff wo filter on ip add
        # sniff(iface=self.interface, filter="ip host " + host + " and port 53", prn=self.dnsQuerryHandler, store=0)
        sniff(iface=self.interface, filter="port 53", prn=self.dnsQuerryHandler, store=0)

    def httpQuerry(self, host):
        # TODO - check if host, if not, launch sniff wo filter on ip add
        # sniff(iface=self.interface, filter="ip host " + host + " and port 80", prn=self.httpQuerryHandler, store=0)
        # sniff(iface=self.interface, filter="port 80", lfilter=lambda d: d.src == '08:00:27:54:8b:1b', prn=self.httpQuerryHandler, store=0)
        sniff(iface=self.interface, filter="port 80", prn=self.httpQuerryHandler, store=0)

    def httpsQuerry(self, host):
        # TODO - check if host, if not, launch sniff wo filter on ip add
        sniff(iface=self.interface, filter="port 443", prn=self.httpQuerryHandler, store=0)

#!/usr/bin/python3
import datetime
import threading
from os.path import join, dirname

import pymysql
from python.database import database
from dotenv import load_dotenv
from scapy.all import *
from scapy.layers.dns import DNS, DNSRR
from scapy.layers.inet import IP
from scapy.layers.inet import Ether


class sniffer (threading.Thread):

    def __init__(self, type):
        threading.Thread.__init__(self)
        pymysql.install_as_MySQLdb()
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
            if self.db.connection == "sqlite":
                sql = "INSERT INTO DNSQueries (ip, domain, datetime) VALUES (?,?,?)"
            elif self.db.connection == "mysql":
                sql = "INSERT INTO DNSQueries (ip, domain, datetime) VALUES (%s, %s, %s)"
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

        # if Ether in pkt :
        #     logging.debug("mac : " + pkt[IP].src +" "+ pkt[Ether].src + "->" + pkt[IP].dst +" "+ pkt[Ether].dst)

        if self.db.connection == "sqlite":
            sql = "select domain from DNSQueries WHERE ip = ? LIMIT 1"
        elif self.db.connection == "mysql":
            sql = "SELECT domain FROM DNSQueries WHERE ip = %s LIMIT 1"

        ret = self.db.execquery(sql, values)

        inverted = False
        if ret == "" or ret is False:
            # sql = "SELECT domain FROM  DNSQueries WHERE ip_dst = %s LIMIT 1"
            values = [str(ip_src)]
            ret = self.db.execquery(sql, values)
            inverted = True
            if ret == "" or ret is False :
                logging.warning("No corresponding domain")
            return

        ret = ret.replace("'", "").replace("(", "").replace(")", "").replace(",", "")
        now = datetime.datetime.now()
        if self.db.connection == "sqlite":
            sql = "INSERT INTO HTTPQueries (mac_iot, domain, datetime) VALUES (?,?,?)"
        elif self.db.connection == "mysql":
            sql = "INSERT INTO HTTPQueries (mac_iot, domain, datetime) VALUES (%s, %s, %s)"
        if not inverted:
            logging.info(pkt[Ether].src + " -> " + ret)
            # values = [str(ip_src), str(ret), now]
            values = [str(pkt[Ether].src), str(ret), now]
        else:
            # values = [str(ip_dst), str(ret), now]
            values = [str(pkt[Ether].dst), str(ret), now]
            logging.info(pkt[Ether].dts + " -> " + ret)

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

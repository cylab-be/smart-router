#!/usr/bin/python3
import datetime
import logging
import os
import socket
import threading
from os.path import join, dirname

import pymysql
from database import database
from dotenv import load_dotenv
from scapy.all import *
from scapy.layers.dns import DNS, DNSRR
from scapy.layers.inet import IP


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
    def run(self):
        logging.info("run")
        logging.info("type = " + self.type)
        if (self.type == "dns"):
            self.dnsQuerry(self.host)
        elif (self.type == "http"):
            self.httpQuerry(self.host)

    def setType(self, host):
        self.host = host

    def dnsQuerryHandler(self, pkt):
        if IP not in pkt: return
        ip_dst = pkt[IP].dst
        if not pkt.haslayer(DNS): return
        if not pkt.ancount > 0 and not isinstance(pkt.an, DNSRR): return
        dest = pkt.an.rdata
        name = str(pkt.getlayer(DNS).qd.qname.decode("utf-8"))
        if not name.endswith('.'): pass
        name = name[:-1]
        try:
            socket.inet_aton(dest)
            logging.debug(ip_dst + "->" + name + "(" + dest + ")")
            now = datetime.datetime.now()
            values = [str(ip_dst), str(dest), str(name), now]
            sql = "INSERT INTO DNSQueries (ip_iot, ip_dst, domain, datetime) VALUES (%s, %s, %s, %s)"
            if self.db.execquery(sql, values):
                logging.error("failed inserting tuple in database")
            else:
                logging.info("new entry in database")
        except socket.error:
            # has no ip address field
            pass
        except TypeError:
            pass

    def httpQuerryHandler(self, pkt):
        if IP not in pkt: return
        ip_dst = pkt[IP].dst
        ip_src = pkt[IP].src
        # logging.info("HTTP sniffer - " + ip_src + "->" + ip_dst)
        sql = "SELECT domain FROM  DNSQueries WHERE ip_dst = %s LIMIT 1"
        ret = self.db.execquery(sql, ip_dst)
        inverted = False
        if ret == "" :
            sql = "SELECT domain FROM  DNSQueries WHERE ip_dst = %s LIMIT 1"
            ret = self.db.execquery(sql, ip_src)
            inverted = True
            if ret == "": logging.warning("No corresponding domain"); return

        ret = ret.replace("'", "").replace("(", "").replace(")", "").replace(",", "")
        now = datetime.datetime.now()
        sql = "INSERT INTO HTTPQueries (ip_iot, domain, datetime) VALUES (%s, %s, %s)"
        if not inverted:
            logging.info(ip_src + " -> " + ret)
            values = [str(ip_src), str(ret), now]
        else:
            values = [str(ip_dst), str(ret), now]
            logging.info(ip_dst + " -> " + ret)
        ret = self.db.execquery(sql, values)


        #
        #     logging.error("failed selecting tuple in database")
        # else:
        #     logging.info("new entry in database")



    def dnsQuerry(self, host):
        sniff(iface=self.interface, filter="ip host " + host + " and port 53", prn=self.dnsQuerryHandler, store=0)

    def httpQuerry(self, host):
        sniff(iface=self.interface, filter="ip host " + host + " and port 80", prn=self.httpQuerryHandler, store=0)

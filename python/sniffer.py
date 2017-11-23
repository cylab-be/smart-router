#!/usr/bin/python3
from scapy.all import *
from scapy.layers.inet import UDP, IP
from scapy.layers.dns import DNS, DNSQR, DNSRR
import socket
import datetime
import logging
import os
from os.path import join, dirname
from dotenv import load_dotenv
from database import database
import pymysql


class sniffer:
    def __init__(self):
        pymysql.install_as_MySQLdb()
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        self.logfile = os.environ.get("LOGFILE")
        logging.basicConfig(filename=self.logfile, level=logging.DEBUG, format='%(asctime)s %(levelname)s - %(message)s')
        self.interface = os.environ.get("INTERFACE")
        self.db = database()
        self.db.connect()

    def dnsQuerryHandler(self, pkt):
        if IP in pkt:
            ip_dst = pkt[IP].dst
            if pkt.haslayer(DNS) :
                if pkt.ancount > 0 and isinstance(pkt.an, DNSRR):
                    dest = (pkt.an.rdata)
                    name = str((pkt.getlayer(DNS).qd.qname).decode("utf-8"))
                    if name.endswith('.'):
                        name = name[:-1]
                    try:
                        socket.inet_aton(dest)
                        logging.debug(ip_dst + "->" + name + "(" + dest + ")")
                        now = datetime.datetime.now()
                        values = [str(ip_dst), str(dest), str(name), now]
                        sql = "INSERT INTO DNSQueries (ip_iot, ip_dst, domain, datetime) VALUES (%s, %s, %s, %s)"
                        if self.db.execquery(sql,values) == False :
                            logging.error("failed inserting tuple in database")
                        else:
                            logging.info("new entry in database")
                    except socket.error:
                        # has no ip address field
                        pass
                    except TypeError:
                        pass
                else:
                    pass



    def dnsQuerry (self, host):
        sniff(iface=self.interface, filter="ip host "+ host +" and port 53", prn=self.dnsQuerryHandler, store=0)





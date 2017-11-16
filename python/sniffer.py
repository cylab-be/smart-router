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
pymysql.install_as_MySQLdb()




class sniffer:
    def __init__(self):
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
            # ip_src = pkt[IP].src
            # print(ip_src + "->" + ip_dst)
            # if pkt.haslayer(DNS) and pkt.getlayer(DNS).qr == 0:
            # print str(ip_src) + " -> " + str(ip_dst) + " : " + "(" + pkt.getlayer(DNS).qd.qname + ")"
            if pkt.haslayer(DNS):
                if pkt.ancount > 0 and isinstance(pkt.an, DNSRR):
                    name = (pkt.an.rdata)
                    try:
                        socket.inet_aton(name)
                        logging.info(ip_dst + "->" + name)
                        now = datetime.datetime.now()
                        values = [str(ip_dst), str(name), now]
                        sql = "INSERT INTO DNSQueries (ip_iot, ip_dst, datetime) VALUES (%s, %s, %s)"
                        if self.db.execquery(sql,values) == False :
                            logging.error("failed inserting tuple in database")
                        else:
                            logging.info("New entry in database")
                    except socket.error:
                        # has no ip address field
                        pass
                    except TypeError:
                        pass
                else:
                    pass



    def dnsQuerry (self, host):
        sniff(iface=self.interface, filter="ip host "+ host +" and port 53", prn=self.dnsQuerryHandler, store=0)





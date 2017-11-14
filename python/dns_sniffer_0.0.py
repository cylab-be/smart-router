from scapy.all import *
from scapy.layers.inet import UDP, IP
from scapy.layers.dns import DNS, DNSQR
import socket
import sys
import pymysql
import datetime
pymysql.install_as_MySQLdb()
import MySQLdb

from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

INTERFACE = os.environ.get("INTERFACE")
DB_HOST = os.environ.get("DB_HOST")
DB_USERNAME = os.environ.get("DB_USERNAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_DATABASE = os.environ.get("DB_DATABASE")

db = MySQLdb.connect(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_DATABASE)

def querysniff(pkt):
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
                    print (ip_dst + "->" + name)
                    cur = db.cursor()
                    now = datetime.datetime.now()
                    values = [str(ip_dst), str(name), now]
                    sql = "INSERT INTO DNSQueries (ip_iot, ip_dst, datetime) VALUES (%s, %s, %s)"
                    cur.execute(sql, values)
                    db.commit()
                    cur.close()
                except socket.error:
                    # has no ip address field
                    pass
                except TypeError:
                    pass
            else:
                pass


sniff(iface=INTERFACE, filter="port 53", prn=querysniff, store=0)
print ("\n[*] Shutting Down...")

#!/usr/bin/python3
import datetime
import threading
from os.path import join, dirname
from dotenv import load_dotenv
from scapy.all import *
from scapy.layers.dns import DNS, DNSRR
from scapy.layers.inet import IP
from scapy.layers.inet import Ether
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
#import pymysql
from python.httpquery import httpquery
from python.database import database


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
        # dispatching differents type of sniffers
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

        try :
            socket.inet_aton(dest)
        except (TypeError, OSError) :
            # Not a correct packet
            return
        now = datetime.datetime.now()
        dns_querry = httpquery([dest, domain, str(now)])
        #Add domain only if ipx domain not present in dns querry table, can be changed by using addTable() function
        if self.db.insertOrIgnoreIntoTable("dnsqueries", dns_querry.toTuple()):
            logging.info("new entry in database(DNS) : " + domain)
        else:
            logging.error("failed inserting DNS tuple in database")

    def httpQuerryHandler(self, pkt):
        # In not an L3 packet, drop it
        if IP not in pkt: return
        ip_dst = pkt[IP].dst
        ip_src = pkt[IP].src

        # Capture only SYN packets
        SYN = 0x02
        if not pkt['TCP'].flags == SYN: return

        # FIXME - Tghe first time tho domain is reached, it is add to DNS tables, beacause of this addition, first request to DNS table can return False if DB is to "slow" to add the DNS entry and commit it
        time.sleep(2)

        # if else condition to determine in wich sense to packet is going (iot->server or server->iot)
        domain = self.db.getDomainFromIp(str(ip_dst))
        if domain :
            ip = str(pkt[Ether].dst)
        else:
            domain = self.db.getDomainFromIp(str(ip_src))
            if not domain :
                # Using ip dst if no domains available to not lose data
                # BEGIN - EXPERIMENTAL REVERSE DNS LOOKUP FEATURE
                #FIXME - experimental feature
                logging.warning("No corresponding domain for "+ip_dst+", resolving ip ...")#("+ip_dst+")")#, using "+ip_dst+" instead")
                now = datetime.datetime.now()
                domain = socket.getfqdn(ip_dst)
                # END - EXPERIMENTAL REVERSE DNS LOOKUP FEATURE
                # logging.debug("Resolved ip "+ ip_dst +" added as " + domain)
                try :
                    # determine if "domain" is a domain or just an ip address
                    socket.inet_aton(domain)
                    domain = "UNRESOLVED("+ip_dst+")"
                except OSError :
                    # if exception, domain is domain and not an ip address
                    pass
                # create a new dnsquery object and store it into the db
                dns_querry = httpquery([ip_dst, domain, str(now)])
                self.db.insertOrIgnoreIntoTable("dnsqueries", dns_querry.toTuple())
            ip = str(pkt[Ether].src)

        now = datetime.datetime.now()
        # create a new httpquery object and store it into the db
        http_querry = httpquery([ip, domain, str(now)])
        if not self.db.insertOrIgnoreIntoTable("httpqueries", http_querry.toTuple()):
            logging.error("failed inserting HTTP tuple in database")
        else:
            logging.info("new entry in database(HTTP(s)) : " + domain)



    def dnsQuerry(self):
        sniff(iface=self.interface, filter="port 53", prn=self.dnsQuerryHandler, store=0)

    def httpQuerry(self):
        sniff(iface=self.interface, filter="port 80", prn=self.httpQuerryHandler, store=0)

    def httpsQuerry(self):
        sniff(iface=self.interface, filter="port 443", prn=self.httpQuerryHandler, store=0)

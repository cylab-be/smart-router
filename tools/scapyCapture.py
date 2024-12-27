from scapy.all import *
from tools.urlChecker import check_urlhaus

def analyzer(packet):
    check_urlhaus(packet)


def start_capture(interface):
    sniff(iface=interface, prn=analyzer)
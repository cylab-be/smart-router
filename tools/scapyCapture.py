from scapy.all import *
from tools.urlChecker import check_urlhaus
from tools.identifyDevices import identify_devices

def analyzer(packet):
    check_urlhaus(packet)
    identify_devices(packet)


def start_capture(interface):
    sniff(iface=interface, prn=analyzer)
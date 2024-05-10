from scapy.all import *

def packet_handler(packet):
    wrpcap("network_traffic.pcap", packet, append=True)

def main():
    # Filtrer les paquets en fonction de l'interface et de l'adresse IP source
    interface = "en0"
    #interface = "etn0"

    # Capture des paquets
    '''Focus on my personal computer'''
    # filter_str = "host 192.168.1.21"
    #sniff(iface=interface, filter=filter_str, prn=packet_handler, store=0)
    sniff(iface=interface, prn=packet_handler, store=0)

if __name__ == '__main__':
    main()
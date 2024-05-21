import scapy.all as scapy

def process_dns(packet):
    if packet.haslayer(scapy.DNS) and packet[scapy.DNS].qr == 0:
        dns_qr = packet[scapy.DNSQR]
        dns_qname = dns_qr.qname.decode("utf-8")
        dns_qtype = scapy.dnsqtypes[dns_qr.qtype]
        print("DNS query:", dns_qname, ", Type:", dns_qtype)
        # add in a list
        # if already in the list don't check again in the json of urlhaus (30 days)


def main():
    print("Sniffing DNS queries...")
    scapy.sniff(filter="udp port 53", prn=process_dns, store=False)

if __name__ == "__main__":
    main()

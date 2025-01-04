from scapy.all import *
import socket
import csv
from mac_vendor_lookup import MacLookup
from dashboard.models import DiscoveredDevice

# Dictionary to store discovered MAC addresses
discovered_macs = []

# Initialize MacLookup
mac_lookup = MacLookup()
mac_lookup.update_vendors()

# All protocols name with their port number
protocols = {}

def get_protocol_name(port, transport_protocol):
    global protocols
    if not protocols:
        protocols = load_protocol_database("./tools/service-names-port-numbers.csv")

    if str(port) in protocols[transport_protocol]:
        if protocols[transport_protocol][str(port)] != '':
            return protocols[transport_protocol][str(port)]
    return "Unknown"

def load_protocol_database(filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            port = row['Port Number']
            protocol = row['Transport Protocol']
            service = row['Service Name']
            if protocol not in protocols:
                protocols[protocol] = {}
            protocols[protocol][port] = service
    return protocols

def identify_protocol(packet):
    if packet.haslayer(IP):
        src_ip = packet[IP].src
        if src_ip.startswith('192.168.'):
            if packet.haslayer(TCP) or packet.haslayer(UDP):
                if packet.haslayer(TCP):
                    proto_layer = packet[TCP]
                    transport_protocol = "tcp"
                else:
                    proto_layer = packet[UDP]
                    transport_protocol = "udp"

                dst_port = proto_layer.dport

                # Use socket to determine the protocol
                protocol = get_protocol_name(dst_port, transport_protocol)

                if protocol != "Unknown":
                    if DiscoveredDevice.objects.filter(src_ip=src_ip).exists():
                        # Update the device's protocols in the database
                        device = DiscoveredDevice.objects.get(src_ip=src_ip)
                        if protocol.upper() not in device.protocols:
                            print(f"Protocol detected: {protocol.upper()} on port {dst_port} from IP: {src_ip}")
                            device.protocols.append(protocol.upper())
                            device.save()
    return None

def get_hostname(ip):
    try:
        # Reverse DNS request
        hostname = socket.gethostbyaddr(ip)[0]
        # Need to remove .lan added by OpenWRT
        if ".lan" in hostname:
            hostname = hostname.split(".lan")[0]
    except socket.herror:
        hostname = "Unknown"
    return hostname

# Not necessary for this project using a OpenWrT router.
# If used, the device must reconnect to the network to be detected!
'''
# Function to analyze DHCP packets
def detect_dhcp_devices(packet):
    if packet.haslayer(DHCP):
        mac_address = packet[Ether].src
        hostname = None

        # Browse DHCP options to find the hostname
        for opt in packet[DHCP].options:
            if opt[0] == 'hostname':  # Option 12 : Hostname
                hostname = opt[1]
                break

        # Display device information
        if hostname:
            print(f"Device detected by DHCP: MAC={mac_address}, Hostname={hostname}")
'''

def check_mac(mac):
    try:
        vendor = mac_lookup.lookup(mac)
        return vendor
    except KeyError:
        return "Unknown"

def identify_devices(packet):
    # hostname = detect_dhcp_devices(packet) # read the comment of the function
    if packet.haslayer(Ether) and packet.haslayer(IP):
        src_mac = packet[Ether].src
        src_ip = packet[IP].src
        if src_ip.startswith('192.168.') and src_mac not in discovered_macs:
            discovered_macs.append(src_mac)
            hostname = get_hostname(src_ip)
            vendor_name = check_mac(src_mac)
            print(f"New MAC discovered: {src_mac} with local IP: {src_ip}, hostname: {hostname}, vendor name: {vendor_name}")

            # Save to the database
            if not DiscoveredDevice.objects.filter(src_mac=src_mac).exists():
                DiscoveredDevice.objects.create(
                    src_mac=src_mac,
                    src_ip=src_ip,
                    hostname=hostname,
                    vendor_name=vendor_name
                )
    identify_protocol(packet)
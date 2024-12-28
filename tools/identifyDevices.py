from scapy.all import *
import socket
from mac_vendor_lookup import MacLookup

# Dictionary to store discovered MAC addresses
discovered_macs = []

# Initialize MacLookup
mac_lookup = MacLookup()
mac_lookup.update_vendors()

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
from scapy.all import *
import re


def capture_mac_ip(interface):
    mac_ip_dict = {}
    # Capture le trafic sur l'interface spécifiée
    packets = sniff(iface=interface, count=10)  # Modifier le nombre de paquets à capturer si nécessaire
    # Parcourt chaque paquet capturé
    for packet in packets:
        # Vérifie si le paquet contient une adresse MAC de destination et une adresse IP source
        if packet.haslayer('Ether') and packet.haslayer('IP'):
            # Récupère l'adresse MAC de destination et l'adresse IP source
            mac = packet[Ether].src
            ip = packet[IP].src
            # Ajoute l'adresse MAC et son adresse IP associée au dictionnaire
            if mac not in mac_ip_dict:
                mac_ip_dict[mac] = ip
    return mac_ip_dict


def capture_arp(interface):
    mac_ip_dict = {}
    # Capture le trafic ARP sur l'interface spécifiée
    packets = sniff(iface=interface, filter="arp", count=10)  # Modifier le nombre de paquets à capturer si nécessaire
    # Parcourt chaque paquet capturé
    for packet in packets:
        # Vérifie si le paquet est une requête ARP et contient l'adresse MAC et IP source
        if ARP in packet and packet.op == 1:
            # Récupère l'adresse MAC et l'adresse IP associée à partir de la requête ARP
            mac = packet.hwsrc
            ip = packet.psrc
            # Ajoute l'adresse MAC et son adresse IP associée au dictionnaire
            if mac not in mac_ip_dict:
                mac_ip_dict[mac] = ip
    return mac_ip_dict

def capture_mac(interface):
    mac_list = []
    # Capture the traffic on the interface of the router
    packets = sniff(iface=interface, count=10)  # Modifier le nombre de paquets à capturer si nécessaire
    for packet in packets:
        print(packet['Ether'])
        # Verify if the packet contains a destination MAC address
        if packet.haslayer('Ether'):
            # Add the mac address to the list if it is not already presents
            if packet['Ether'].dst not in mac_list:
                mac_list.append(packet['Ether'].dst)
    return mac_list

def check_mac(mac_address):
    # Verify if the MAC address is valid
    mac_pattern = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
    if mac_pattern.match(mac_address):
        return True
    else:
        return False

if __name__ == "__main__":
    interface = "en0"  # Spécifiez l'interface réseau à utiliser, en0 pour Ethernet sur macOS
    mac_ip_dict = capture_arp(interface)
    print("Liste des adresses MAC et leurs adresses IP associées à partir des requêtes ARP :")
    for mac, ip in mac_ip_dict.items():
        print("MAC :", mac, "- IP :", ip)

    '''    
    interface = "en0"  # Spécifiez l'interface réseau à utiliser, en0 pour Ethernet sur macOS
    mac_ip_dict = capture_mac_ip(interface)
    print("Liste des adresses MAC et leurs adresses IP associées :")
    for mac, ip in mac_ip_dict.items():
        print("MAC :", mac, "- IP :", ip)'''

    #mac_addresses.append('Z4:0c:25:e2:80:10') -> bad mac address
    '''for mac in mac_addresses:
        if check_mac(mac):
            print(f"L'adresse MAC {mac} est valide.")
        else:
            print(f"L'adresse MAC {mac} n'est pas valide.")'''
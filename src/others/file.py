from scapy.all import *
import hashlib

def calculate_sha256(file_content):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(file_content)
    return sha256_hash.hexdigest()

def process_http(packet):
    if packet.haslayer('TCP') and packet.haslayer('Raw'):
        payload = packet[Raw].load.decode("utf-8", errors="ignore")
        if "GET" in payload and "HTTP" in payload:
            # Extraction de l'URL demandée dans la requête GET
            start_index = payload.find("GET") + 4
            end_index = payload.find("HTTP")
            url = payload[start_index:end_index].strip()

            # Extraction du nom de fichier à partir de l'URL
            file_name = url.split("/")[-1]
            print(file_name)
    
            # Calcul du hash du fichier si c'est une image
            if file_name.endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp")):
                file_content = b""
                if packet.haslayer(Raw):
                    file_content += packet[Raw].load
                    sha256_hash = calculate_sha256(file_content)
                    print("Téléchargement détecté :")
                    print("Nom du fichier :", file_name)
                    print("SHA256 :", sha256_hash)
                    print()

def start_capture(interface):
    sniff(iface=interface, prn=process_http, filter="tcp port 80 or tcp port 443")

if __name__ == "__main__":
    interface = "en0"  # Spécifiez l'interface réseau à utiliser, en0 pour Ethernet sur macOS
    start_capture(interface)

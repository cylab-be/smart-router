import requests
import json
from scapy.all import *


def query_urlhaus(url):
    # Construct the HTTP request
    data = {'url': url}
    response = requests.post('https://urlhaus-api.abuse.ch/v1/url/', data)
    # Parse the response from the API
    json_response = response.json()
    return json_response


def process_http(packet):
    if packet.haslayer('TCP') and packet.haslayer('Raw'):
        payload = packet[Raw].load.decode("utf-8", errors="ignore")
        if "GET" in payload and "HTTP" in payload:
            # Extraction du nom de domaine à partir de l'URL
            start_index = payload.find("Host: ") + 6
            end_index = payload.find("\r\n", start_index)
            host = payload[start_index:end_index].strip()

            # Extraction de l'URL demandée dans la requête GET
            start_index = payload.find("GET") + 4
            end_index = payload.find("HTTP")
            url = payload[start_index:end_index].strip()

            if host.find("www.") == 1:
                full_url = host.replace("www.", "") + url
            else:
                full_url = host + url

            print("URL demandée :", full_url)
            # improve for http://buycodeshop.com/ and http://buycodeshop.com/.nttpd%2C6-arm-le-t1-z
            # improve for http://scan.nperm.net/thinkphp
            # https://heko.ro/ProjectE_5.exe
            # trouver + d'info que l'url précise avec URLhaus

            # Recherche de l'URL sur l'API URLhaus
            response = query_urlhaus("http://" + full_url)
            if response['query_status'] == 'ok':    # and his online (big alert) his offline small alert
                print(json.dumps(response, indent=4, sort_keys=False))  # show all the data
                # can extract the type of the malware for example
                tags = ""
                for tag in response['tags']:
                    tags += tag + " "
                print("Alert: " + tags)
            elif response['query_status'] == 'no_results':
                print("No results")
            else:
                print("Something went wrong")


def start_capture(interface):
    sniff(iface=interface, prn=process_http)


if __name__ == "__main__":
    interface = "br-lan"  # Spécifiez l'interface réseau à utiliser, en0 pour Ethernet sur macOS
    start_capture(interface)
    #print(query_urlhaus("https://heko.ro/ProjectE_5.exe"))

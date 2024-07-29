import requests
import json
from scapy.all import *
from django.utils import timezone
from dashboard.models import MaliciousURL

def query_urlhaus(url):
    data = {'url': url}
    response = requests.post('https://urlhaus-api.abuse.ch/v1/url/', data)
    json_response = response.json()
    return json_response

def process_http(packet):
    if packet.haslayer('IP') and packet.haslayer('TCP') and packet.haslayer('Raw'):
        src_ip = packet[IP].src
        payload = packet[Raw].load.decode("utf-8", errors="ignore")
        if "GET" in payload and "HTTP" in payload:
            start_index = payload.find("Host: ") + 6
            end_index = payload.find("\r\n", start_index)
            host = payload[start_index:end_index].strip()

            start_index = payload.find("GET") + 4
            end_index = payload.find("HTTP")
            url = payload[start_index:end_index].strip()

            if host.find("www.") == 1:
                full_url = host.replace("www.", "") + url
            else:
                full_url = host + url

            print(f"URL requested: {full_url} from IP: {src_ip}")

            response = query_urlhaus("http://" + full_url)
            if response['query_status'] == 'ok':
                tags = " ".join(response['tags'])
                MaliciousURL.objects.create(url=full_url, malware_type=tags, detected_at=timezone.now(), source_ip=src_ip)
            elif response['query_status'] == 'no_results':
                print(url)
                print("No results")
            else:
                print(url)
                print("Something went wrong")

def start_capture(interface):
    sniff(iface=interface, prn=process_http)

if __name__ == "__main__":
    interface = "en0"
    start_capture(interface)
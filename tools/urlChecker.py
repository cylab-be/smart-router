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

def define_priority(url_status, date_added):
    date_format = "%Y-%m-%d %H:%M:%S %Z"
    date_added = datetime.strptime(date_added, date_format)
    days_diff = (datetime.utcnow() - date_added).days

    if url_status == "online" or days_diff <= 7:
        return "high"
    elif url_status == "offline" and days_diff <= 90:
        return "medium"
    elif url_status == "offline" and days_diff > 90:
        return "low"
    else:
        return "low"

def analyzer(packet):
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
                if response['urlhaus_reference']:
                    reference_url = response['urlhaus_reference']
                else:
                    reference_url = "None"
                if response['tags']:
                    tags = " ".join(response['tags'])
                else:
                    tags = "no information"
                if response['url_status']:
                    url_status = response['url_status']
                if response['date_added']:
                    date_added = response['date_added']
                priority = define_priority(url_status, date_added)
                MaliciousURL.objects.create(
                    url=full_url,
                    malware_type=tags,
                    detected_at=timezone.now(),
                    source_ip=src_ip,
                    reference_url=reference_url,
                    priority=priority
                )
            elif response['query_status'] == 'no_results':
                print(url)
                print("No results")
            else:
                print(url)
                print("Something went wrong")

def start_capture(interface):
    sniff(iface=interface, prn=analyzer)
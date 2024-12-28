from django.http import HttpResponse
from django.shortcuts import render

from .models import MaliciousURL, SnortAlert, DiscoveredDevice

def index(request):
    malicious_urls = MaliciousURL.objects.all()
    snort_alerts = SnortAlert.objects.all()
    malicious_url_count = MaliciousURL.objects.count()
    snort_alert_count = SnortAlert.objects.count()
    unique_internal_ips = get_unique_internal_ips()
    infected_device_count = len(unique_internal_ips)
    discovered_devices = DiscoveredDevice.objects.all()

    priority_map = {1: 'high', 2: 'medium', 3: 'low'}
    for alert in snort_alerts:
        alert.priority_label = priority_map.get(alert.priority, 'unknown')

    for alert in malicious_urls:
        alert.priority_label = alert.priority

    return render(request, "dashboard/index.html", {
        "malicious_urls": malicious_urls,
        "snort_alerts": snort_alerts,
        "malicious_url_count": malicious_url_count,
        "snort_alert_count": snort_alert_count,
        "infected_device_count": infected_device_count,
        'discovered_devices': discovered_devices
    })

def get_unique_internal_ips():
    malicious_ips = MaliciousURL.objects.values_list('source_ip', flat=True).distinct()
    snort_ips = SnortAlert.objects.values_list('src_ip', flat=True).distinct()
    unique_ips = set(malicious_ips).union(set(snort_ips))
    local_ips = {ip for ip in unique_ips if ip.startswith('192.168.')}
    return local_ips
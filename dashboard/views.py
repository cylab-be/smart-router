from django.http import HttpResponse
from django.shortcuts import render

from .models import MaliciousURL, SnortAlert

def index(request):
    malicious_urls = MaliciousURL.objects.all()
    snort_alerts = SnortAlert.objects.all()
    malicious_url_count = MaliciousURL.objects.count()
    snort_alert_count = SnortAlert.objects.count()

    priority_map = {1: 'high', 2: 'medium', 3: 'low'}
    for alert in snort_alerts:
        alert.priority_label = priority_map.get(alert.priority, 'unknown')

    for alert in malicious_urls:
        alert.priority_label = alert.priority

    return render(request, "dashboard/index.html", {
        "malicious_urls": malicious_urls,
        "snort_alerts": snort_alerts,
        "malicious_url_count": malicious_url_count,
        "snort_alert_count": snort_alert_count
    })
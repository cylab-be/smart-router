from django.http import HttpResponse
from django.shortcuts import render

from .models import MaliciousURL, SnortAlert

import threading
from signature_analysis.url import start_capture


def index(request):
    malicious_urls = MaliciousURL.objects.all()
    snort_alerts = SnortAlert.objects.all()
    return render(request, "dashboard/index.html", {"malicious_urls": malicious_urls, "snort_alerts": snort_alerts})

def start_network_monitor(request):
    interface = "en0"
    thread = threading.Thread(target=start_capture, args=(interface,))
    thread.daemon = True
    thread.start()
    return HttpResponse("Network monitoring started.")
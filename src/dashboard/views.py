from django.http import HttpResponse
from django.shortcuts import render
import threading
from signature_analysis.url import start_capture


def index(request):
    return render(request, "dashboard/index.html")

def start_network_monitor(request):
    interface = "en0"
    thread = threading.Thread(target=start_capture, args=(interface,))
    thread.daemon = True
    thread.start()
    return HttpResponse("Network monitoring started.")
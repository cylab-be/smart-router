from django.apps import AppConfig

def startup():
    import threading
    interface = "br-lan"    # Change this to the interface you want to monitor, for OpenWRT it is usually "br-lan"

    from tools.scapyCapture import start_capture
    thread = threading.Thread(target=start_capture, args=(interface,))
    thread.daemon = True
    thread.start()

    from tools.snort.snortProcessor import run_snort
    thread = threading.Thread(target=run_snort, args=(interface,))
    thread.daemon = True
    thread.start()

class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'

    def ready(self):
        import os
        if os.environ.get('RUN_MAIN'):
            startup()
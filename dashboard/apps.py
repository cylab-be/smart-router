from django.apps import AppConfig

def startup():
    import threading
    from tools.url import start_capture
    interface = "br-lan"
    thread = threading.Thread(target=start_capture, args=(interface,))
    thread.daemon = True
    thread.start()

    from tools.snort.launch import run_snort
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
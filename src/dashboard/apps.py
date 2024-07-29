from django.apps import AppConfig

def startup():
    import threading
    from signature_analysis.url import start_capture
    interface = "en0"
    thread = threading.Thread(target=start_capture, args=(interface,))
    thread.daemon = True
    thread.start()

class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'

    def ready(self):
        import os
        if os.environ.get('RUN_MAIN'):
            startup()
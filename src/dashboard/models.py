from django.db import models

class MaliciousURL(models.Model):
    url = models.CharField(max_length=255)
    malware_type = models.CharField(max_length=255)
    detected_at = models.DateTimeField(auto_now_add=True)
    source_ip = models.GenericIPAddressField()

    def __str__(self):
        return self.url
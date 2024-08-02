from django.db import models

class MaliciousURL(models.Model):
    url = models.CharField(max_length=255)
    malware_type = models.CharField(max_length=255)
    detected_at = models.DateTimeField(auto_now_add=True)
    source_ip = models.GenericIPAddressField()
    reference_url = models.URLField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.url

class SnortAlert(models.Model):
    timestamp = models.DateTimeField()
    alert_name = models.CharField(max_length=255)
    classification = models.CharField(max_length=255)
    priority = models.IntegerField()
    src_ip = models.GenericIPAddressField()
    src_port = models.IntegerField()
    dest_ip = models.GenericIPAddressField()
    dest_port = models.IntegerField()
from django.db import models

class MaliciousURL(models.Model):
    url = models.CharField(max_length=255)
    malware_type = models.CharField(max_length=255)
    detected_at = models.DateTimeField(auto_now_add=True)
    source_ip = models.GenericIPAddressField()
    reference_url = models.URLField(max_length=255)
    priority = models.CharField(max_length=10)

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

class DiscoveredDevice(models.Model):
    src_mac = models.CharField(max_length=17, unique=True)
    src_ip = models.GenericIPAddressField()
    hostname = models.CharField(max_length=255)
    vendor_name = models.CharField(max_length=255)
    protocols = models.JSONField(default=list)

    def __str__(self):
        return f"{self.hostname} ({self.src_mac})"
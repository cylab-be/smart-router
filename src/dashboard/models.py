from django.db import models

class MaliciousSite(models.Model):
    url = models.CharField(max_length=255)
    malware_type = models.CharField(max_length=255)
    detected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url
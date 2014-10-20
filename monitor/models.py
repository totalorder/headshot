from django.utils import timezone
from django.db import models


# Create your models here.
class Monitor(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    type = models.CharField(max_length=255)
    description = models.TextField()

    def getLastStatus(self):
        return self.statuses.order_by('-timestamp')[:1].get()


class Status(models.Model):
    OK = "OK"
    WARN = "Warn"
    FAILED = "Failed"
    INVALID = "Invalid"

    monitor = models.ForeignKey(Monitor, related_name="statuses", null=False)
    code = models.CharField(max_length=32,
                            choices=(tuple((field, field) for field in (OK, WARN, FAILED, INVALID))),
                            null=False)
    short_desc = models.CharField(max_length=128, null=False)
    desc = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
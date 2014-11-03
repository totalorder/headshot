from django.utils import timezone
from django.db import models


# Create your models here.
class Monitor(models.Model):
    class Envs:
        DEV = 'dev'
        TST = 'tst'
        TRN = 'trn'
        PRD = 'prd'

    environment = models.CharField(max_length=3, null=False, blank=False, choices=(
        (Envs.DEV, Envs.DEV),
        (Envs.TST, Envs.TST),
        (Envs.TRN, Envs.TRN),
        (Envs.PRD, Envs.PRD)))
    interval = models.IntegerField(null=False)
    description = models.TextField()
    image = models.TextField(default="front/images/db.gif")

    def getLastStatus(self):
        return self.statuses.order_by('-timestamp')[:1].get()

    def __unicode__(self):
        return self.description


class URLMonitor(Monitor):
    url = models.CharField(max_length=4096, null=False)
    warn_latency = models.IntegerField(null=False)


class LocalProcessMonitor(Monitor):
    command = models.TextField(null=False)
    success_message = models.CharField(max_length=128, null=False)


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
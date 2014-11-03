from django.contrib import admin
from monitor.models import URLMonitor, LocalProcessMonitor


class URLMonitorAdmin(admin.ModelAdmin):
    pass

admin.site.register(URLMonitor, URLMonitorAdmin)


class LocalProcessMonitorAdmin(admin.ModelAdmin):
    pass

admin.site.register(LocalProcessMonitor, LocalProcessMonitorAdmin)
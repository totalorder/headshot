from itertools import chain
from django.shortcuts import render

# Create your views here.
from monitor.models import URLMonitor, LocalProcessMonitor


def index(request):
    return render(request, 'index.html', {'monitors': chain(URLMonitor.objects.all(), LocalProcessMonitor.objects.all())})

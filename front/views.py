from django.shortcuts import render

# Create your views here.
from monitor.models import Monitor


def index(request):
    return render(request, 'index.html', {'monitors': Monitor.objects.all()})

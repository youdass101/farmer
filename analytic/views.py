from django.shortcuts import render
from farmer.models import *
from .helper.helper import today_plan
from datetime import date, timedelta
from django.utils import timezone
from farmer.models import Harvest

# Dashboard page
def dashboard(request):
    context = today_plan()
    return render(request, 'dashboard.html', context)

def output_graph(request):
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=730)
    qs = Harvest.objects.filter(date__range=(start_date, end_date)).order_by('date')
    dates = [h.date.strftime('%Y-%m-%d') for h in qs]
    outputs = [h.output for h in qs]
    return render(request, 'graph.html', {'dates': dates, 'outputs': outputs})
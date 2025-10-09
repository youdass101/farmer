from django.shortcuts import render
from farmer.models import *
from .helper.helper import today_plan
# Dashboard page
def dashboard(request):
    print("Dashboard accessed")
    context = today_plan()
    return render(request, 'dashboard.html', context)
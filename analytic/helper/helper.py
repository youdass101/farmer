from django.shortcuts import render
from django.db.models import Avg, Count
from farmer.models import Tray, Harvest, Plant
from datetime import date, timedelta
from django.utils import timezone



def today_plan():
    # Group by Tray.name, calculate average number per day
    today = timezone.now()
    #django_weekday = today.weekday() + 2  # Python Monday=0, Django Monday=2
    # trays = Tray.objects.filter(name__active=True, start__week_day=django_weekday)
    end_date = timezone.now()
    start_date = (end_date - timedelta(days=80)).date()  # 1 year
    print(start_date)
    trays = Tray.objects.filter(name__active=True, start=start_date)

    tray_stats = (
        trays.values('name__name')
        .annotate(
            total_trays=Count('id'),
            #total_weeks=0,  #Count('start__week', distinct=True),
            avg_per_week=Count('id')  #Count('id') / Count('start__week', distinct=True)
        )
    )
    context = {
        'today' : today,
        'weekday': today.strftime('%A'),
        'tray_stats': tray_stats
    }
    print(context)
    return context


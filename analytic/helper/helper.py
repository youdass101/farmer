from django.shortcuts import render
from django.db.models import Avg, Count
from farmer.models import Tray
from datetime import date, timedelta
from django.utils import timezone
from farmer.models import Harvest


def today_plan():
    # Group by Tray.name, calculate average number per day
    today = date.today()
    django_weekday = today.weekday() + 2  # Python Monday=0, Django Monday=2
    trays = Tray.objects.filter(name__active=True, start__week_day=django_weekday)
    tray_stats = (
        trays.values('name__name')
        .annotate(
            total_trays=Count('id'),
            total_weeks=Count('start__week', distinct=True),
            avg_per_week=Count('id') / Count('start__week', distinct=True)
        )
    )
    context = {
        'today' : today,
        'weekday': today.strftime('%A'),
        'tray_stats': tray_stats
    }
    print(context)
    return context
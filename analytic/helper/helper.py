from django.shortcuts import render
from django.db.models import Avg, Count
from farmer.models import Tray
from datetime import date

def today_plan():
    # Group by Tray.name, calculate average number per day
    tray_stats = (
        Tray.objects.values('name__name')  # If name is FK to Plant, use 'name__name'
        .annotate(
            avg_number=Avg('number'),
            total_days=Count('start', distinct=True)
        )
    )
    today = date.today()
    # Prepare context for template
    context = {
        'today': today,
        'tray_stats': tray_stats,
    }
    return context
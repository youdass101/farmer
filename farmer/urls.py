from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("plants", views.plants, name="plants"),
    path("medium", views.medium, name="medium"),
    path("harvest", views.harvest, name="harvest"),
    path("history", views.history, name="history"),
    path("report", views.report, name="report"),
]
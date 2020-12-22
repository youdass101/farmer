from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("plants", views.plants, name="plants"),
    path("medium", views.medium, name="medium"),
    path("harvest", views.harvest, name="harvest"),
    path("history", views.history, name="history"),
    path("filter", views.filter, name="filter"),
    path("analytics", views.analytics, name="analytics"),
]
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('output-graph', views.output_graph, name='output_graph'),
]
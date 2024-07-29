from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("start-monitoring/", views.start_network_monitor, name="start_monitoring"),
]
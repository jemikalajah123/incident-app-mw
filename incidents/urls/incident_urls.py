from django.urls import path
from incidents.views import incident_views as views

urlpatterns = [

    path('', views.getIncidents, name="incidents"),
]

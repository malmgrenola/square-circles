from django.urls import path
from . import views

urlpatterns = [
    path('', views.reservations, name='reservations'),
    path('set_availability/', views.set_availability, name='set_availability'),
]

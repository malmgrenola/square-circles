from django.urls import path
from . import views

urlpatterns = [
    path('', views.reservation, name='reservation'),
    path('add/<int:product_id>/', views.add_reservation, name='add_reservation'),
    path('remove/<int:reservation_index>/',
         views.remove_reservation, name='remove_reservation'),
    path('set_travel_info/', views.set_travel_info, name='set_travel_info'),
]

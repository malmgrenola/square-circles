from django.urls import path
from . import views

urlpatterns = [
    path('', views.basket, name='basket'),
    path('add/<int:product_id>/', views.add_product, name='add_product'),
    path('remove/<int:basket_index>/',
         views.remove_product, name='remove_product'),
    path('set_travel_info/', views.set_travel_info, name='set_travel_info'),
]

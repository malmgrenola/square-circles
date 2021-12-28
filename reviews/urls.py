from django.urls import path
from . import views

urlpatterns = [
    path('', views.reviews, name='reviews'),
    path('review/<int:review_id>/change',
         views.change, name='change'),
    path('review/add',
         views.add, name='add'),
    path('review/<int:review_id>/delete',
         views.delete, name='delete'),
]

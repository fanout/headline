from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),
    path('<int:headline_id>/', views.item, name='item'),
]

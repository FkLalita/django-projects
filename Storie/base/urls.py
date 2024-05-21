from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('read/<int:pk>/', views.Read_story, name='read_story'),
    path('search/', views.search, name='search'),
    path('latest/', views.home_latest, name='latest')
]
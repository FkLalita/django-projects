from django.urls import path
from . import views


urlpatterns = [
    path('task-home/', views.taskHome, name='task_home'),
    path('', views.home, name='home'),
    path('task-view/<str:pk>/', views.taskView, name='task_view'),
    path('task-create/', views.taskCreate, name='task_create'),
    path('task-update/<str:pk>/', views.taskUpdate, name='task_update'),
    path('task-delete/<str:pk>/', views.taskDelete, name='task_delete'),
    path('signup/', views.signup, name='signuppage'),
    path('login/', views.loginpage, name='loginpage'),    
    path('logout/', views.logoutuser, name='logout'),


]

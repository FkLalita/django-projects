from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('question/<int:pk>/', views.question_detail, name='question_detail'),
    path('question/<int:pk>/answer/', views.answer_question, name='answer_question'),
    path('ask/', views.ask_question, name='ask_question'),
    path('question/<int:pk>/answer/<int:answer_id>/', views.answer_detail, name='answer_detail'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search, name='search'),
    path('user/', views.user_profile, name='user_profile'),
    path('user/edit/', views.edit_profile, name='edit_profile'),
]

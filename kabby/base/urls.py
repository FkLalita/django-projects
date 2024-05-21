from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('locations/', views.location, name='location'),
    path('locations/add/', views.add_location, name='add_location'),
    path('locations/<int:pk>/', views.edit_location, name='edit_location'),
    path('rides/', views.Rides, name='rides'),
    path('rides/book/', views.book_ride, name='book_ride'),
    path('rides/<int:pk>/', views.view_ride, name='view_ride'),
    path('rides/<int:pk>/complete/', views.complete_ride, name='complete_ride'),
    path('drivers/', views.driver, name='drivers'),
    path('drivers/add/', views.add_driver, name='add_driver'),
    path('drivers/<int:pk>/', views.edit_driver, name='edit_driver'),
    path('fund-wallet/', views.fund_wallet, name='fund_wallet'),
    path('payment/', views.payment, name='payment'),
]

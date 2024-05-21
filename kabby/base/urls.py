from django.urls import path
from .views import PassengerSignupView, DriverSignupView, LoginView, LogoutView, \
    DashboardView, RideCreateView, RideListView, RideDetailView, PaymentView

app_name = 'base'

urlpatterns = [
    path('passenger/signup/', PassengerSignupView.as_view(), name='passenger_signup'),
    path('driver/signup/', DriverSignupView.as_view(), name='driver_signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('ride/create/', RideCreateView.as_view(), name='ride_create'),
    path('ride/list/', RideListView.as_view(), name='ride_list'),
    path('ride/detail/<int:pk>/', RideDetailView.as_view(), name='ride_detail'),
    path('ride/detail/<int:pk>/pay/', PaymentView.as_view(), name='payment'),
]

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Passenger, Driver, Ride

class PassengerSignupForm(UserCreationForm):
    phone_number = forms.CharField(max_length=20)
    payment_method = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'phone_number', 'payment_method')

class DriverSignupForm(UserCreationForm):
    car_model = forms.CharField(max_length=50)
    license_plate = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'car_model', 'license_plate')

class RideForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = ('pickup_address', 'dropoff_address', 'pickup_time', 'distance')

class PaymentForm(forms.Form):
    payment_method = forms.ChoiceField(choices=(('Credit Card', 'Credit Card'), ('PayPal', 'PayPal')))
    card_number = forms.CharField(max_length=20)
    card_cvv = forms.CharField(max_length=4)
    card_expiry = forms.CharField(max_length=5, help_text='Format: MM/YY')


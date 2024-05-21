from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Profile, Location, Ride, Driver

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    mobile_number = forms.CharField(max_length=20, help_text='Required. Enter a valid mobile number.')
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'mobile_number', 'password1', 'password2', )

class EditProfileForm(UserChangeForm):
    password = None
    mobile_number = forms.CharField(max_length=20, help_text='Required. Enter a valid mobile number.')
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'mobile_number', )

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ('name', 'address', 'location_city', 'location_state', 'location_country', 'location_zipcode', )

class EditLocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ('name', 'address', 'location_city', 'location_state', 'location_country', 'location_zipcode', )

class RideForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = ('pickup_location', 'dropoff_location' )

class CompleteRideForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = ('ride_status', )

class AddDriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ('name', 'phone_number', 'license_plate' )

class EditDriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ('name', 'phone_number', 'license_plate' )


class FundWalletForm(forms.Form):
    amount = forms.DecimalField(max_digits=6, decimal_places=2)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, label='Username')
    password = forms.CharField(max_length=50, label='Password', widget=forms.PasswordInput)

class PaymentForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
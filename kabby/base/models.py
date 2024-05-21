from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=20)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)

    def __str__(self):
        return self.user.username

class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    latitude =  models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    location_country = models.CharField(max_length=50)    
    location_city = models.CharField(max_length=50)
    location_zipcode = models.IntegerField()
    location_state = models.CharField(max_length=50)

 
    def __str__(self):
        return self.name

class Driver(models.Model):
    name = models.CharField(max_length=100, default='John Doe')
    phone_number = models.CharField(max_length=20)
    car_type = models.CharField(max_length=100,default='Bus' )
    car_model = models.CharField(max_length=100, default='Jeep')
    car_color = models.CharField(max_length=100, default='Blue')
    license_plate = models.CharField(max_length=20)
    profile_picture = models.ImageField(upload_to='drivers/', null=True, blank=True)

    def __str__(self):
        return self.name

class Ride(models.Model):
    passenger = models.ForeignKey(User, on_delete=models.CASCADE)
    pickup_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='pickup_location')
    dropoff_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='dropoff_location')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True, blank=True)
    ride_status = models.CharField(max_length=50, default='REQUESTED')
    ride_status = models.CharField(max_length=50, default='REQUESTED') 
    ride_created = models.DateTimeField(auto_now_add=True)
    ride_completed = models.DateTimeField(null=True, blank=True)
    payment_status = models.CharField(max_length=50, default='UNPAID')
    fare = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.passenger.username} - {self.ride_created}"


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s Wallet"


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    timestamp = models.DateTimeField(auto_now_add=True)

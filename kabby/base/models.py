from django.db import models
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Passenger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    car_model = models.CharField(max_length=50)
    license_plate = models.CharField(max_length=20)
    rating = models.FloatField(default=0)

    def __str__(self):
        return self.user.username

class Ride(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    pickup_address = models.CharField(max_length=200)
    dropoff_address = models.CharField(max_length=200)
    pickup_time = models.DateTimeField()
    ride_time = models.DateTimeField(blank=True, null=True)
    distance = models.FloatField()
    fare = models.FloatField()
    payment_status = models.CharField(max_length=20, default='UNPAID')
    rating = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.passenger.user.username} - {self.driver.user.username}'

    def save(self, *args, **kwargs):
        if self.payment_status == 'PAID':
            # do payment
            pass
        super(Ride, self).save(*args, **kwargs)

from django.contrib import admin
from .models import Ride,Location,Driver,Profile,Wallet

# Register your models here

admin.site.register (Location)
admin.site.register (Ride)
admin.site.register (Profile)
admin.site.register (Driver)
admin.site.register (Wallet)



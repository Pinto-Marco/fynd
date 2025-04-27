from django.contrib import admin
from . import models


# Register your models here.

admin.site.register(models.Activity) 
admin.site.register(models.BookingSearch)
admin.site.register(models.SavedAccommodation)

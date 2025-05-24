from django.contrib import admin
from . import models


# Register your models here.

admin.site.register(models.Activity) 
admin.site.register(models.Locale)
# admin.site.register(models.BookingSearch)
# admin.site.register(models.SavedAccommodation)
admin.site.register(models.FynderBasicCard)
admin.site.register(models.Schedule)
admin.site.register(models.Tag)
admin.site.register(models.FynderTag)

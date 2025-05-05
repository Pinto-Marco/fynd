from django.contrib import admin
from . import models as trip_models

# Register your models here.
admin.site.register(trip_models.TripQuestion)
admin.site.register(trip_models.TripType)
admin.site.register(trip_models.Trip)
admin.site.register(trip_models.TripFynder)
admin.site.register(trip_models.TripQuestionAnswer)

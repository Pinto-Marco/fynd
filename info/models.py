from django.db import models
from fynder import models as fynder_models 
from trip import models as trip_models
import requests
from django.conf import settings
VIATOR_API_URL = settings.VIATOR_API_URL
VIATOR_API_KEY = settings.VIATOR_API_KEY
from . import viator_client


class Activity(models.Model):
    ACTIVITY_TYPES = (
        ('Cibo', 'Cibo'),
        ('Must see culturali', 'Must see culturali'),
        ('Eventi', 'Eventi'),
        ('Escursioni', 'Escursioni'),
        ('Museo', 'Museo'),
        ('Tour', 'Tour'),
        ('Parco', 'Parco'),
        ('Mercato', 'Mercato'),
        ('Negozi particolari', 'Negozi particolari'),
        ('Spa', 'Spa'),
        ('Spiaggia', 'Spiaggia'),
    )

    # Fields from the API of Viator
    productCode = models.CharField(max_length=255, null=True, blank=True)

    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPES, null=True, blank=True)
    generation_category = models.CharField(max_length=50, choices=trip_models.TripType.GENERATION_CATEGORIES, null=True, blank=True)

    # Interest Categories
    interest_culture_heritage = models.BooleanField(default=False)
    interest_nature_outdoors = models.BooleanField(default=False)
    interest_food_gastronomy = models.BooleanField(default=False)
    interest_nightlife_party = models.BooleanField(default=False)
    interest_wellness_spa = models.BooleanField(default=False)
    # interest_sport_adventure = models.BooleanField(default=False)
    # interest_music_festivals = models.BooleanField(default=False)
    # interest_shopping_fashion = models.BooleanField(default=False)


    # Activity-specific fields just for Activity created by other fynders and to be approved by the operator
    # fynder_creator = models.ForeignKey(fynder_models.Fynder, on_delete=models.CASCADE,  null=True, blank=True)
    # fynder_approver = models.ForeignKey(fynder_models.Fynder, on_delete=models.CASCADE, null=True, blank=True)
    # website = models.URLField(blank=True, null=True)
    # address = models.CharField(max_length=255, blank=True, null=True)
    # phone_number = models.CharField(max_length=20, blank=True, null=True)
    # email = models.EmailField(blank=True, null=True)
    # opening_hours = models.TextField(blank=True, null=True)
    # duration = models.DurationField(blank=True, null=True)
    # image = models.ImageField(upload_to='activity_images/', blank=True, null=True)
    # min_pax = models.PositiveIntegerField(blank=True, null=True)
    # max_pax = models.PositiveIntegerField(blank=True, null=True)
    # price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)


    def __str__(self):
        return self.name

    def fetch_viator_product_code(self):
        return viator_client.fetch_viator_product_code(self.productCode)

    def get_local(self):
        local = Locale.objects.filter(activity_ref=self).first()
        if local:
            return local
        else:
            return None

    def get_type(self):
        if self.activity_type:
            if self.activity_type == 'Cibo':
                local = self.get_local()
                if local:
                    return local.service_type
                else:
                    return None
            else:
                return self.activity_type
        else:
            return None



class Locale(models.Model):

    LOCALE_TYPES = (
        ('Ristorante', 'Ristorante'),
        ('Street food', 'Street food'),
        ('Cucino a casa', 'Cucino a casa'),
        ('Bar caffetteria', 'Bar caffetteria'),
        ('Disco', 'Disco'),
        ('Pub', 'Pub'),
        ('Coffe shop', 'Coffe shop'),
    )
    SERVICE_TYPES = (
        ('Pasticceria', 'Pasticceria'),
        ('Aperitivi', 'Aperitivi'),
        ('Chioschi', 'Chioschi'),
        ('Enoteche', 'Enoteche'),
        ('Colazione', 'Colazione'),
        ('Brunch', 'Brunch'),
        ('Cena', 'Cena'),
        ('Pranzo', 'Pranzo'),
        ('Eventi', 'Eventi'),
    )
    CUISINE_TYPES = (
        ('Italiana', 'Italiana'),
        ('Cinese', 'Cinese'),
        ('Giapponese', 'Giapponese'),
        ('Indiana', 'Indiana'),
        ('Americana', 'Americana'),
        ('Araba', 'Araba'),
        ('Mediterranea', 'Mediterranea'),
        ('Messicana', 'Messicana'),
        ('Pesce', 'Pesce'),
        ('Fast food', 'Fast food'),
        ('Pizzeria', 'Pizzeria'),
    )

    activity_ref = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='locale')
    type = models.CharField(max_length=50, choices=LOCALE_TYPES, null=True, blank=True)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPES, null=True, blank=True)
    cuisine_type = models.CharField(max_length=50, choices=CUISINE_TYPES, null=True, blank=True)


class FynderBasicType(models.Model):
    name = models.CharField(max_length=50)
    img = models.ImageField(upload_to='fynder-basic-types/', null=True, blank=True)
    description = models.TextField()
    interest_culture_heritage = models.FloatField(default=0.00, help_text="Interest level in Culture & Heritage (0-100)")
    interest_nature_outdoors = models.FloatField(default=0.00, help_text="Interest level in Nature & Outdoors (0-100)")
    interest_food_gastronomy = models.FloatField(default=0.00, help_text="Interest level in Food & Gastronomy (0-100)")
    interest_nightlife_party = models.FloatField(default=0.00, help_text="Interest level in Nightlife & Party (0-100)")
    interest_wellness_spa = models.FloatField(default=0.00, help_text="Interest level in Wellness & Spa (0-100)")
    # interest_sport_adventure = models.FloatField(default=0.00, help_text="Interest level in Sport & Adventure (0-100)")
    # interest_music_festivals = models.FloatField(default=0.00, help_text="Interest level in Music & Festivals (0-100)")
    # interest_shopping_fashion = models.FloatField(default=0.00, help_text="Interest level in Shopping & Fashion (0-100)")

    def __str__(self):
        return self.name

    def get_tags(self):
        tags = FynderTag.objects.filter(fynder_basic_type=self)
        if tags:
            return [tag.tag for tag in tags]
        else:
            return []

    def get_schedules(self):
        schedules = Schedule.objects.filter(fynder_basic_type=self).order_by('start_date')
        if schedules:
            return schedules
        else:
            return []

class Tag(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class FynderTag(models.Model):
    fynder_basic_type = models.ForeignKey(FynderBasicType, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return self.tag.name + " - " + str(self.fynder_basic_type)
    
class Schedule(models.Model):
    SCHEDULE_TYPES = (
        ('Activity', 'Activity'),
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
    )

    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    type = models.CharField(max_length=50, choices=SCHEDULE_TYPES, null=True, blank=True)
    fynder_basic_type = models.ForeignKey(FynderBasicType, on_delete=models.CASCADE)

    def __str__(self):
        return self.type + " - " + str(self.start_date) + " - " + str(self.end_date) + " - " + str(self.fynder_basic_type)

    

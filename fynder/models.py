from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta

class Fynder(AbstractUser):
    GENDER_CHOICES = (
        ('male', 'male'),
        ('female', 'female'),
        ('other', 'other'),
        ('prefer_not_to_say', 'prefer_not_to_say'),
    )

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    has_new_letter = models.BooleanField(default=False)
    gender = models.CharField(max_length=17, choices=GENDER_CHOICES, default='prefer_not_to_say')
    age = models.PositiveIntegerField(null=True, blank=True)
    country_of_origin = models.CharField(max_length=100, blank=True, null=True)
    is_vegetarian = models.BooleanField(default=False)
    is_vegan = models.BooleanField(default=False)
     # Interest Categories (stored as percentages)
    interest_culture_heritage = models.FloatField(default=0.00, help_text="Interest level in Culture & Heritage (0-100)")
    interest_nature_outdoors = models.FloatField(default=0.00, help_text="Interest level in Nature & Outdoors (0-100)")
    interest_food_gastronomy = models.FloatField(default=0.00, help_text="Interest level in Food & Gastronomy (0-100)")
    interest_nightlife_party = models.FloatField(default=0.00, help_text="Interest level in Nightlife & Party (0-100)")
    interest_wellness_spa = models.FloatField(default=0.00, help_text="Interest level in Wellness & Spa (0-100)")
    interest_sport_adventure = models.FloatField(default=0.00, help_text="Interest level in Sport & Adventure (0-100)")
    interest_music_festivals = models.FloatField(default=0.00, help_text="Interest level in Music & Festivals (0-100)")
    interest_shopping_fashion = models.FloatField(default=0.00, help_text="Interest level in Shopping & Fashion (0-100)")
    
class FoodPreference(models.Model):
    FOOD_PREFERENCE_CHOICES = (
        ('Any', 'Any'),
        ('Pescatarian', 'Pescatarian'),
        ('Halal', 'Halal'),
        ('Kosher', 'Kosher'),
    )
    fynder = models.ForeignKey(Fynder, on_delete=models.CASCADE)
    label = models.CharField(max_length=20, choices=FOOD_PREFERENCE_CHOICES, default='any')

class TemporaryCode(models.Model):
    user = models.OneToOneField(Fynder, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=2)

    def _str_(self):
        return f"Temporary Code for {self.user.email}"


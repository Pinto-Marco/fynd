from django.db import models

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
    )

    GENERATION_CATEGORIES = (
        ('Any', 'Any'),
        ('Vacanza al Mare', 'Vacanza al Mare'),
        ('Avventura in Montagna', 'Avventura in Montagna'),
        ('City Break Culturale', 'City Break Culturale'),
        ('City Break Locale', 'City Break Locale'),
        ('Viaggio Notturno e di Divertimento', 'Viaggio Notturno e di Divertimento'),
        ('Ritiro di Benessere in Natura', 'Ritiro di Benessere in Natura'),
        ('Viaggio di Lusso', 'Viaggio di Lusso'),
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPES)
    generation_category = models.CharField(max_length=50, choices=GENERATION_CATEGORIES)

    # Interest Categories (stored as percentages)
    interest_culture_heritage = models.FloatField(default=0.00, help_text="Interest level in Culture & Heritage (0-100)")
    interest_nature_outdoors = models.FloatField(default=0.00, help_text="Interest level in Nature & Outdoors (0-100)")
    interest_food_gastronomy = models.FloatField(default=0.00, help_text="Interest level in Food & Gastronomy (0-100)")
    interest_nightlife_party = models.FloatField(default=0.00, help_text="Interest level in Nightlife & Party (0-100)")
    interest_wellness_spa = models.FloatField(default=0.00, help_text="Interest level in Wellness & Spa (0-100)")
    interest_sport_adventure = models.FloatField(default=0.00, help_text="Interest level in Sport & Adventure (0-100)")
    interest_music_festivals = models.FloatField(default=0.00, help_text="Interest level in Music & Festivals (0-100)")
    interest_shopping_fashion = models.FloatField(default=0.00, help_text="Interest level in Shopping & Fashion (0-100)")

    # Activity-specific fields
    website = models.URLField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    opening_hours = models.TextField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)
    image = models.ImageField(upload_to='activity_images/', blank=True, null=True)
    min_pax = models.PositiveIntegerField(blank=True, null=True)
    max_pax = models.PositiveIntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)


    def __str__(self):
        return self.name
    
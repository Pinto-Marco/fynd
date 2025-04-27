from django.db import models
from fynder.models import Fynder

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


class BookingSearch(models.Model):
    fynder = models.ForeignKey(Fynder, on_delete=models.CASCADE)
    # Required fields
    checkin = models.DateField()
    checkout = models.DateField()
    adults = models.IntegerField(default=2)
    rooms = models.IntegerField(default=1)
    
    # Location fields
    city_id = models.IntegerField(null=True)
    country = models.CharField(max_length=2, null=True)  # ISO2 country code
    district = models.IntegerField(null=True)
    region = models.IntegerField(null=True)
    airport = models.CharField(max_length=3, null=True)  # IATA code
    
    # Guest details
    children = models.JSONField(null=True, help_text="Array of children ages [5, 8]")
    guest_allocation = models.JSONField(null=True, help_text="Exact allocation of guests to rooms")
    
    # Filters
    accommodation_types = models.JSONField(null=True, help_text="Array of accommodation type IDs")
    accommodation_facilities = models.JSONField(null=True, help_text="Array of facility IDs")
    room_facilities = models.JSONField(null=True, help_text="Array of room facility IDs")
    brands = models.JSONField(null=True, help_text="Array of hotel chain IDs")
    
    # Price and payment
    currency = models.CharField(max_length=3, null=True)  # ISO currency code
    min_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    max_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    payment_type = models.CharField(max_length=20, null=True, choices=[
        ('pay_at_property', 'Pay at Property'),
        ('pay_online', 'Pay Online')
    ])
    credit_card_required = models.BooleanField(default=False)
    
    # Meal and cancellation
    meal_plan = models.CharField(max_length=20, null=True, choices=[
        ('all_inclusive', 'All Inclusive'),
        ('breakfast_included', 'Breakfast Included'),
        ('full_board', 'Full Board'),
        ('half_board', 'Half Board')
    ])
    cancellation_type = models.CharField(max_length=20, null=True, choices=[
        ('free_cancellation', 'Free Cancellation'),
        ('non_refundable', 'Non Refundable')
    ])
    
    # Additional filters
    min_review_score = models.IntegerField(null=True)
    stars = models.JSONField(null=True, help_text="Array of star ratings [4, 5]")
    twenty_four_hour_reception = models.BooleanField(default=False)
    travel_proud = models.BooleanField(default=False, help_text="LGBTQ+ friendly properties")
    
    # Sorting
    sort_by = models.CharField(max_length=20, null=True, choices=[
        ('distance', 'Distance'),
        ('price', 'Price'),
        ('review_score', 'Review Score'),
        ('stars', 'Stars')
    ])
    sort_direction = models.CharField(max_length=20, null=True, choices=[
        ('ascending', 'Ascending'),
        ('descending', 'Descending')
    ])
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Search for {self.fynder.email} in city {self.city_id}"


class SavedAccommodation(models.Model):
    fynder = models.ForeignKey(Fynder, on_delete=models.CASCADE)
    booking_id = models.IntegerField()
    search = models.ForeignKey(BookingSearch, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    deep_link_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    main_photo_url = models.URLField(null=True, blank=True)
    photos = models.JSONField(null=True, blank=True, help_text="Array of photo URLs")

    def __str__(self):
        return f"{self.name} - {self.price} {self.currency}"
    
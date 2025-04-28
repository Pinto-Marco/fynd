from django.db import models
from fynder import models as fynder_models

# Create your models here.
class TripQuestion(models.Model):
    QUESTION_TYPE_CHOICES = (
        ('pax', 'pax'),
        ('where', 'where'),
        ('when', 'when'),
        ('budget', 'budget'),
        ('intensity', 'intensity'),
    )
    question_text = models.CharField(max_length=200)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES)

    def __str__(self):
        return self.question_text

class Trip(models.Model):

    TRIP_PAX_TYPE_CHOICES = (
        ('singolo', 'singolo'),
        ('amici', 'amici'),
        ('famiglia', 'famiglia'),
        ('coppia', 'coppia'),
    )
    TRIP_INTENSITY_CHOICES = (
        ('poco','poco'),
        ('medio', 'medio'),
        ('tanto', 'tanto')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    trip_pax_type = models.CharField(max_length=20, choices=TRIP_PAX_TYPE_CHOICES, default='singolo')
    location = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    trip_intensity = models.CharField(max_length=20, choices=TRIP_INTENSITY_CHOICES, default='medio')

    def get_fynders(self):
        trip_fynders = TripFynder.objects.filter(trip=self)
        return [trip_fynder.fynder for trip_fynder in trip_fynders]

    def get_trip_types(self):
        trip_types = TripType.objects.filter(trip=self)
        return [trip_type.generation_category for trip_type in trip_types]



class TripType(models.Model):

    GENERATION_CATEGORIES = (
        ('Any', 'Any'),
        ('Vacanza al Mare', 'Vacanza al Mare'),
        ('Avventura in Montagna', 'Avventura in Montagna'),
        ('City Break Culturale', 'City Break Culturale'),
        ('City Break Locale', 'City Break Locale'),
        ('Viaggio Notturno e di Divertimento', 'Viaggio Notturno e di Divertimento'),
        ('Ritiro di Benessere in Natura', 'Ritiro di Benessere in Natura'),
        ('Viaggio di Lusso', 'Viaggio di Lusso'),
        ('Vacanza con Macchina', 'Vacanza con Macchina'),
    )
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    generation_category = models.CharField(max_length=50, choices=GENERATION_CATEGORIES, default='Any')
    
class TripFynder(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    fynder = models.ForeignKey(fynder_models.Fynder, on_delete=models.CASCADE)

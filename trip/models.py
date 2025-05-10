from django.db import models
from fynder import models as fynder_models

# Create your models here.
class TripQuestion(models.Model):
    QUESTION_TYPE_CHOICES = (
        ('pax', 'pax'),
        ('where', 'where'),
        ('from', 'from'),
        ('when', 'when'),
        ('budget', 'budget'),
        ('intensity', 'intensity'),
    )
    question_text = models.CharField(max_length=200)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES)

    def __str__(self):
        return self.question_text

    def get_answers(self):
        answers = list(TripQuestionAnswer.objects.filter(question=self))
        if not answers:
            return []
        return [answer.answer for answer in answers]

class TripQuestionAnswer(models.Model):
    question = models.ForeignKey('TripQuestion', on_delete=models.CASCADE)
    answer = models.CharField(max_length=200)

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
    TRIP_STATUS_CHOICES = (
        ('pending', 'pending'),
        ('active', 'active'),
        ('completed', 'completed'),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=TRIP_STATUS_CHOICES, default='pending')

    trip_pax_type = models.CharField(max_length=20, choices=TRIP_PAX_TYPE_CHOICES, default='singolo')
    from_location = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    trip_intensity = models.CharField(max_length=20, choices=TRIP_INTENSITY_CHOICES, default='medio')

    def get_fynders(self):
        trip_fynders = TripFynder.objects.filter(trip=self)
        return [trip_fynder.fynder for trip_fynder in trip_fynders]

    def get_trip_types(self):
        trip_types = TripType.objects.filter(trip=self)
        return [trip_type.generation_category for trip_type in trip_types]

class TripFynderAnswer(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    question = models.ForeignKey(TripQuestion, on_delete=models.CASCADE)
    answer = models.CharField(max_length=200)


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
    is_owner = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        # prendere tutti i trip_fynders con lo stesso trip, se non ci sono più, eliminare il trip
        trip_fynders = TripFynder.objects.filter(trip=self.trip)
        if len(trip_fynders) == 1:
            self.trip.delete()
        if self.is_owner:
            # se il trip_fynder corrente è l'owner, impostare il primo trip_fynder come owner
            trip_fynder = TripFynder.objects.filter(trip=self.trip).first()
            if trip_fynder:
                trip_fynder.is_owner = True
                trip_fynder.save()

        super().delete(*args, **kwargs)

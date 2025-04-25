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

    def __str__(self):
        return self.username

    def get_all_sign_up_answers(self):
        answers = SignUpFynderAnswer.objects.filter(fynder=self)
        if not answers:
            return []
        return answers

    def get_all_sign_up_answers_by_question_id(self, question_id):
        answers = SignUpFynderAnswer.objects.filter(fynder=self, answer__question_id=question_id)
        if not answers:
            return []
        return answers

    def delete_all_sign_up_answers_by_question_id(self, question_id):
        answers = SignUpFynderAnswer.objects.filter(fynder=self.id, answer__question_id=question_id)
        if answers:
            for answer in answers:
                answer.delete()

    
class FynderFoodPreference(models.Model):
    FOOD_PREFERENCE_CHOICES = (
        ('Any', 'Any'),
        ('Pescatarian', 'Pescatarian'),
        ('Halal', 'Halal'),
        ('Kosher', 'Kosher'),
    )
    fynder = models.ForeignKey(Fynder, on_delete=models.CASCADE)
    label = models.CharField(max_length=20, choices=FOOD_PREFERENCE_CHOICES, default='any')

    def __str__(self):
        return self.label

class TemporaryCode(models.Model):
    user = models.OneToOneField(Fynder, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=2)

    def __str__(self):
        return f"Temporary Code for {self.user.email}"

class SignUpQuestion(models.Model):
    question_text = models.CharField(max_length=200)
    weight = models.FloatField(default=1.0)

    def __str__(self):
        return self.question_text

    def get_all_answers(self):
        answers = SignUpAnswer.objects.filter(question=self)
        if not answers:
            return []
        return answers

class SignUpAnswer(models.Model):
    question = models.ForeignKey(SignUpQuestion, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=200)
    interest_culture_heritage = models.FloatField(default=0.0, help_text="Interest level in Culture & Heritage (0-0.5-1)")
    interest_nature_outdoors = models.FloatField(default=0.0, help_text="Interest level in Nature & Outdoors (0-0.5-1)")
    interest_food_gastronomy = models.FloatField(default=0.0, help_text="Interest level in Food & Gastronomy (0-0.5-1)")
    interest_nightlife_party = models.FloatField(default=0.0, help_text="Interest level in Nightlife & Party (0-0.5-1)")
    interest_wellness_spa = models.FloatField(default=0.0, help_text="Interest level in Wellness & Spa (0-0.5-1)")
    interest_sport_adventure = models.FloatField(default=0.0, help_text="Interest level in Sport & Adventure (0-0.5-1)")
    interest_music_festivals = models.FloatField(default=0.0, help_text="Interest level in Music & Festivals (0-0.5-1)")
    interest_shopping_fashion = models.FloatField(default=0.0, help_text="Interest level in Shopping & Fashion (0-0.5-1)")


    def __str__(self):
        return f"{self.question.question_text}: {self.answer_text}"

class SignUpFynderAnswer(models.Model):
    fynder = models.ForeignKey(Fynder, on_delete=models.CASCADE)
    answer = models.ForeignKey(SignUpAnswer, on_delete=models.CASCADE)

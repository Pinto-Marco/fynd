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
    

class TemporaryCode(models.Model):
    user = models.OneToOneField(Fynder, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=2)

    def _str_(self):
        return f"Temporary Code for {self.user.email}"


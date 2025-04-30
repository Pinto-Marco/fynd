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
    # TODO user delete photos and create img_profile field
    # img_profile = models.ImageField(upload_to='profile_images/', blank=True, null=True)
     # Interest Categories (stored as percentages)
    interest_culture_heritage = models.FloatField(default=0.00, help_text="Interest level in Culture & Heritage (0-100)")
    interest_nature_outdoors = models.FloatField(default=0.00, help_text="Interest level in Nature & Outdoors (0-100)")
    interest_food_gastronomy = models.FloatField(default=0.00, help_text="Interest level in Food & Gastronomy (0-100)")
    interest_nightlife_party = models.FloatField(default=0.00, help_text="Interest level in Nightlife & Party (0-100)")
    interest_wellness_spa = models.FloatField(default=0.00, help_text="Interest level in Wellness & Spa (0-100)")
    interest_sport_adventure = models.FloatField(default=0.00, help_text="Interest level in Sport & Adventure (0-100)")
    interest_music_festivals = models.FloatField(default=0.00, help_text="Interest level in Music & Festivals (0-100)")
    interest_shopping_fashion = models.FloatField(default=0.00, help_text="Interest level in Shopping & Fashion (0-100)")

    def get_all_sign_up_answers(self):
        fynder_answers = SignUpFynderAnswer.objects.filter(fynder=self)
        answers = [answer.answer for answer in fynder_answers]
        if not answers:
            return []
        return answers

    def get_all_sign_up_answers_by_question_id(self, question_id):
        fynder_answers = SignUpFynderAnswer.objects.filter(fynder=self, answer__question_id=question_id)
        # return just the answer of SignUpFynderAnswer
        answers = [answer.answer for answer in fynder_answers]
        if not answers:
            return []
        return answers

    def delete_all_sign_up_answers_by_question_id(self, question_id):
        answers = SignUpFynderAnswer.objects.filter(fynder=self.id, answer__question_id=question_id)
        if answers:
            for answer in answers:
                answer.delete()

    def delete_data(self): 
        from trips.models import TripFynder
        all_trips = TripFynder.objects.filter(fynder=self)
        all_food_preferences = FynderFoodPreference.objects.filter(fynder=self)
        all_sign_up_answers = SignUpFynderAnswer.objects.filter(fynder=self)
        all_friendship = Friendship.objects.filter(
            models.Q(fynder_1=request.user, friend_2_id=friend_id) |
            models.Q(fynder_1_id=friend_id, friend_2=request.user)
        )
        if all_trips:
            for trip in all_trips:
                trip.delete()
        if all_food_preferences:
            for food_preference in all_food_preferences:
                food_preference.delete()
        if all_sign_up_answers:
            for sign_up_answer in all_sign_up_answers:
                sign_up_answer.delete()
        if all_friendship:
            for friendship in all_friendship:
                friendship.delete()
        return True

    def set_calculate_interest(self):
        total_interest_culture_heritage = 0.0
        total_interest_nature_outdoors = 0.0
        total_interest_food_gastronomy = 0.0
        total_interest_nightlife_party = 0.0
        total_interest_wellness_spa = 0.0
        total_interest_sport_adventure = 0.0
        total_interest_music_festivals = 0.0
        total_interest_shopping_fashion = 0.0
        questions = SignUpQuestion.objects.all()
        total_weight = 0.0

        for question in questions:
            # prendere il peso della domanda
            weight = question.weight
            total_weight += weight
            # massimo interesse tra tutti i valori
            max_score = weight 
            # prendere tutte le risposte a quella domanda
            sign_up_answers = SignUpFynderAnswer.objects.filter(fynder=self, answer__question_id=question.id)
            # calcolare il numero totale di risposte a quella domande
            total_answers = sign_up_answers.count()
            if total_answers > 0:
                # calcolare la base della domanda (peso / numero risposte)
                base = weight / total_answers
                # azzerare variabili per ogni interesse 
                question_interest_culture_heritage = 0.0
                question_interest_nature_outdoors = 0.0
                question_interest_food_gastronomy = 0.0
                question_interest_nightlife_party = 0.0
                question_interest_wellness_spa = 0.0
                question_interest_sport_adventure = 0.0
                question_interest_music_festivals = 0.0
                question_interest_shopping_fashion = 0.0
                #ciclo su risposte
                for sign_up_answer in sign_up_answers:
                    question_interest_culture_heritage += base * sign_up_answer.answer.interest_culture_heritage
                    question_interest_nature_outdoors += base * sign_up_answer.answer.interest_nature_outdoors
                    question_interest_food_gastronomy += base * sign_up_answer.answer.interest_food_gastronomy
                    question_interest_nightlife_party += base * sign_up_answer.answer.interest_nightlife_party
                    question_interest_wellness_spa += base * sign_up_answer.answer.interest_wellness_spa
                    question_interest_sport_adventure += base * sign_up_answer.answer.interest_sport_adventure
                    question_interest_music_festivals += base * sign_up_answer.answer.interest_music_festivals
                    question_interest_shopping_fashion += base * sign_up_answer.answer.interest_shopping_fashion
                
                if question_interest_culture_heritage > max_score:
                    question_interest_culture_heritage = max_score
                if question_interest_nature_outdoors > max_score:
                    question_interest_nature_outdoors = max_score
                if question_interest_food_gastronomy > max_score:
                    question_interest_food_gastronomy = max_score
                if question_interest_nightlife_party > max_score:
                    question_interest_nightlife_party = max_score
                if question_interest_wellness_spa > max_score:
                    question_interest_wellness_spa = max_score
                if question_interest_sport_adventure > max_score:
                    question_interest_sport_adventure = max_score
                if question_interest_music_festivals > max_score:
                    question_interest_music_festivals = max_score
                if question_interest_shopping_fashion > max_score:
                    question_interest_shopping_fashion = max_score

                total_interest_culture_heritage += question_interest_culture_heritage
                total_interest_nature_outdoors += question_interest_nature_outdoors
                total_interest_food_gastronomy += question_interest_food_gastronomy
                total_interest_nightlife_party += question_interest_nightlife_party
                total_interest_wellness_spa += question_interest_wellness_spa
                total_interest_sport_adventure += question_interest_sport_adventure
                total_interest_music_festivals += question_interest_music_festivals
                total_interest_shopping_fashion += question_interest_shopping_fashion


        if total_weight > 0:
            self.interest_culture_heritage = (total_interest_culture_heritage / total_weight) * 100
            self.interest_nature_outdoors = (total_interest_nature_outdoors / total_weight) * 100
            self.interest_food_gastronomy = (total_interest_food_gastronomy / total_weight) * 100
            self.interest_nightlife_party = (total_interest_nightlife_party / total_weight) * 100
            self.interest_wellness_spa = (total_interest_wellness_spa / total_weight) * 100
            self.interest_sport_adventure = (total_interest_sport_adventure / total_weight) * 100
            self.interest_music_festivals = (total_interest_music_festivals / total_weight) * 100
            self.interest_shopping_fashion = (total_interest_shopping_fashion / total_weight) * 100
            self.save()

        return self

    
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
    max_number_of_answers = models.IntegerField(default=4)

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


class Friendship(models.Model):
    fynder_1 = models.ForeignKey(Fynder, on_delete=models.CASCADE, related_name='fynder_1')
    friend_2 = models.ForeignKey(Fynder, on_delete=models.CASCADE, related_name='fynder_2')
    def __str__(self):
        return f"{self.fynder_1.username} - {self.fynder_2.username}"
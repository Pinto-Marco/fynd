from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from . import models as fynder_models 

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'password', 'gender')
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Aggiunge dati utente al token JWT."""
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data.update({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'gender': user.gender,
        })
        return data

class AllPossibleFoodPreferencesSerializer(serializers.Serializer):
    food_preferences = serializers.ListField(child=serializers.ChoiceField(choices=fynder_models.FoodPreference.FOOD_PREFERENCE_CHOICES))

class UserUpdateSerializer(serializers.ModelSerializer):
    # food_preferences = serializers.ChoiceField(choices=fynder_models.FoodPreference.FOOD_PREFERENCE_CHOICES, required=False)
    food_preferences = serializers.ListField(child=serializers.ChoiceField(choices=fynder_models.FoodPreference.FOOD_PREFERENCE_CHOICES), required=False)

    class Meta:
        model = User
        exclude = ('password', 'is_superuser', 'is_staff', 'last_login', 'is_active', 'date_joined', 'groups', 'user_permissions',
                   )
        read_only_fields = ('interest_culture_heritage', 'interest_nature_outdoors', 'interest_food_gastronomy', 'interest_nightlife_party', 'interest_wellness_spa', 'interest_sport_adventure', 'interest_music_festivals', 'interest_shopping_fashion')

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'food_preferences':
                for food_preference in value:
                    choices=fynder_models.FoodPreference.FOOD_PREFERENCE_CHOICES
                    if food_preference not in [choice[0] for choice in choices]:
                        raise serializers.ValidationError(f"{food_preference} is not a valid food preference.")
                    else:
                        fynder_models.FoodPreference.objects.update_or_create(
                            fynder=instance,
                            label=food_preference,
                            defaults={'label': food_preference}
                        )
            setattr(instance, attr, value)
        instance.save()
        return instance
    
class RequestTemporaryCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

class VerifyTemporaryCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)

class ChangePasswordNewSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, required=True)

class UserProfileSerializer(serializers.ModelSerializer):
    food_preferences = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ('password', 'is_superuser', 'is_staff', 'last_login', 'is_active', 'date_joined', 'groups', 'user_permissions')

    def get_food_preferences(self, obj):
        food_preferences = fynder_models.FoodPreference.objects.filter(fynder=obj)
        return [food_preference.label for food_preference in food_preferences]


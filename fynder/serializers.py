from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'is_superuser', 'is_staff', 'last_login', 'is_active', 'date_joined', 'groups', 'user_permissions')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
class UserUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)  # Non obbligatorio
    username = serializers.CharField(max_length=150, required=False)  # Non obbligatorio
    first_name = serializers.CharField(max_length=150, required=False)  # Non obbligatorio
    last_name = serializers.CharField(max_length=150, required=False)  # Non obbligatorio
    gender = serializers.ChoiceField(choices=User.GENDER_CHOICES, required=False)  # Non obbligatorio
    has_new_letter = serializers.BooleanField(required=False)  # Non obbligatorio

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'gender', 'has_new_letter')

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
class RequestTemporaryCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

class VerifyTemporaryCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)

class ChangePasswordNewSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, required=True)
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
    food_preferences = serializers.ListField(child=serializers.ChoiceField(choices=fynder_models.FynderFoodPreference.FOOD_PREFERENCE_CHOICES))

class UserUpdateSerializer(serializers.ModelSerializer):
    food_preferences = serializers.ListField(child=serializers.ChoiceField(choices=fynder_models.FynderFoodPreference.FOOD_PREFERENCE_CHOICES), required=False)

    class Meta:
        model = User
        exclude = ('password', 'is_superuser', 'is_staff', 'last_login', 'is_active', 'date_joined', 'groups', 'user_permissions',
                   )
        read_only_fields = ('interest_culture_heritage', 'interest_nature_outdoors', 'interest_food_gastronomy', 'interest_nightlife_party', 'interest_wellness_spa', 'interest_sport_adventure', 'interest_music_festivals', 'interest_shopping_fashion')

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'food_preferences':
                for food_preference in value:
                    choices=fynder_models.FynderFoodPreference.FOOD_PREFERENCE_CHOICES
                    if food_preference not in [choice[0] for choice in choices]:
                        raise serializers.ValidationError(f"{food_preference} is not a valid food preference.")
                    else:
                        for choice in choices:
                            old = fynder_models.FynderFoodPreference.objects.filter(fynder=instance, label=choice[0]).first()
                            if old:
                                old.delete()
                        fynder_models.FynderFoodPreference.objects.update_or_create(
                            fynder=instance,
                            label=food_preference,
                            defaults={'label': food_preference}
                        )
            else:
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
        food_preferences = fynder_models.FynderFoodPreference.objects.filter(fynder=obj)
        return [food_preference.label for food_preference in food_preferences]


class PossibleSignUpQuestionAnswerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    question_text = serializers.CharField()
    max_number_of_answers = serializers.IntegerField()
    answers = serializers.SerializerMethodField()

    class Meta:
        model = fynder_models.SignUpQuestion
        fields = ('id', 'question_text', 'max_number_of_answers', 'answers')

    def get_answers(self, obj):
        answers = obj.get_all_answers()
        data = []
        for answer in answers:
            data.append({'id': answer.id, 'answer_text': answer.answer_text})
        return data

class SignUpFynderAnswerSerializer(serializers.ModelSerializer):
    question_id = serializers.IntegerField()
    answers = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        model = fynder_models.SignUpFynderAnswer
        fields = ('question_id', 'answers')

    def validate(self, attrs):
        question_id = attrs.get('question_id')
        answers = attrs.get('answers')
        question = fynder_models.SignUpQuestion.objects.filter(id=question_id).first()
        if not question:
            raise serializers.ValidationError("Invalid question ID")

        max_number_of_answers = question.max_number_of_answers
        answers_count = len(answers)
        if answers_count < 1 or answers_count > max_number_of_answers:
            raise serializers.ValidationError("Answers count must be between 1 and ".format(max_number_of_answers))
        for answer_id in answers:
            answer = fynder_models.SignUpAnswer.objects.filter(id=answer_id).first()
            if not answer:
                raise serializers.ValidationError("Invalid answer ID")
        return attrs

    def create(self, validated_data):
        fynder = validated_data.pop('fynder')
        question_id = validated_data.pop('question_id')
        answer_ids = validated_data.pop('answers')
        
        # Delete existing answers for this question
        fynder.delete_all_sign_up_answers_by_question_id(question_id)
        
        # Create new answers
        created_answers = []
        for answer_id in answer_ids:
            answer = fynder_models.SignUpAnswer.objects.get(id=answer_id)
            answer_obj = fynder_models.SignUpFynderAnswer.objects.create(
                fynder=fynder,
                answer=answer
            )
        
class GetSignUpFynderAnswerSerializer(serializers.ModelSerializer):
    question_id = serializers.SerializerMethodField()
    question_text = serializers.SerializerMethodField()
    answers = serializers.SerializerMethodField()
    
    class Meta:
        model = fynder_models.SignUpFynderAnswer
        fields = ('question_id', 'question_text', 'answers')

    def get_question_id(self, obj):
        return obj.answer.question.id

    def get_question_text(self, obj):
        return obj.answer.question.question_text

    def get_answers(self, obj):
        return [{'id': answer.id, 'answer_text': answer.answer_text} for answer in obj.fynder.get_all_sign_up_answers_by_question_id(obj.answer.question.id)]

class AddFriendLinkSerializer(serializers.Serializer):
    friend_id = serializers.CharField()

    def save(self, **kwargs):
        fynder = self.context['request'].user
        friend_id = self.validated_data.get("friend_id")
        if friend_id:
            friend = User.objects.filter(id=friend_id).first()
            if not friend:
                raise serializers.ValidationError("Invalid friend ID")
            if friend == fynder:
                raise serializers.ValidationError("You cannot add yourself as a friend")
            if fynder_models.Friendship.objects.filter(fynder_1=fynder, friend_2=friend).exists() or fynder_models.Friendship.objects.filter(fynder_1=friend, friend_2=fynder).exists():
                raise serializers.ValidationError("You are already friends with this user")
            else:
                fynder_models.Friendship.objects.create(fynder_1=fynder, friend_2=friend)
        return self.validated_data
        
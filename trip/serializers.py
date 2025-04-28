from rest_framework import serializers
from trip.models import TripQuestion


class TripQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripQuestion
        fields = '__all__'
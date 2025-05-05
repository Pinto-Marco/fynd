from rest_framework import serializers
from trip import models as trip_models


class TripQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = trip_models.TripQuestion
        fields = '__all__'

class TripQuestionAnswerSerializer(serializers.Serializer):
    answer = serializers.CharField()

    # class Meta:
    #     model = TripQuestion
    #     fields = ('question_id', 'answer')

    def validate(self, data):
        question_id = self.context.get('question_id')
        try:
            question = trip_models.TripQuestion.objects.get(id=question_id)
        except trip_models.TripQuestion.DoesNotExist:
            raise serializers.ValidationError("Question not found")

        if question.question_type == 'pax':
            if data['answer'] not in dict(trip_models.Trip.TRIP_PAX_TYPE_CHOICES):
                raise serializers.ValidationError("Invalid pax type")
        elif question.question_type == 'intensity':
            if data['answer'] not in dict(trip_models.Trip.TRIP_INTENSITY_CHOICES):
                raise serializers.ValidationError("Invalid intensity level")
        elif question.question_type == 'when':
            try:
                start_date, end_date = data['answer'].split(',')
                datetime.strptime(start_date.strip(), '%Y-%m-%d')
                datetime.strptime(end_date.strip(), '%Y-%m-%d')
            except (ValueError, IndexError):
                raise serializers.ValidationError("Invalid date format. Use YYYY-MM-DD,YYYY-MM-DD")
        elif question.question_type == 'budget':
            try:
                float(data['answer'])
            except ValueError:
                raise serializers.ValidationError("Budget must be a number")

        data['question'] = question
        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        question = self.validated_data['question']
        answer = self.validated_data['answer']

        # Get or create Trip for the current user
        trip_fynder = trip_models.TripFynder.objects.filter(
            fynder=user
        ).order_by('-trip__created_at').first()

        if not trip_fynder:
            trip = trip_models.Trip.objects.create()
            trip_fynder = trip_models.TripFynder.objects.create(
                trip=trip,
                fynder=user
            )

        # Update Trip based on question type
        trip = trip_fynder.trip
        if question.question_type == 'pax':
            trip.trip_pax_type = answer
        elif question.question_type == 'where':
            trip.location = answer
        elif question.question_type == 'when':
            start_date, end_date = answer.split(',')
            trip.start_date = start_date.strip()
            trip.end_date = end_date.strip()
        elif question.question_type == 'budget':
            trip.budget = float(answer)
        elif question.question_type == 'intensity':
            trip.trip_intensity = answer

        trip.save()
        return trip



    
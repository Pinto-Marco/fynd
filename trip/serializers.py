from rest_framework import serializers
from trip import models as trip_models
from fynder import models as fynder_models


class TripQuestionSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    class Meta:
        model = trip_models.TripQuestion
        fields =  ['id', 'question_text', 'question_type', 'answers']

    def get_answers(self, obj):
        answers = obj.get_answers()
        return [answer for answer in answers]


class TripFynderAnswerSerializer(serializers.Serializer):
    answer = serializers.CharField()
    trip_id = serializers.IntegerField(required=False)

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
        trip_id = self.validated_data['trip_id'] if 'trip_id' in self.validated_data else None

        # Get or create Trip for the current user
        if trip_id is None:
            trip = trip_models.Trip.objects.create()
            trip_id = trip.id
            trip_fynder = trip_models.TripFynder.objects.create(trip=trip, fynder=user, is_owner=True)
        else:
            trip = trip_models.Trip.objects.get(id=trip_id)
            trip_fynder = trip_models.TripFynder.objects.get(trip=trip, fynder=user)

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

        # Create TripQuestionAnswer
        trip_question_answer = trip_models.TripFynderAnswer.objects.create(
            trip=trip,
            question=question,
            answer=answer
        )

        return trip

class TripQuestionAnswerItemSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    answer = serializers.CharField()

class TripFynderAnswerAllTogetherSerializer(serializers.Serializer):
    answers = TripQuestionAnswerItemSerializer(many=True)

    def validate(self, data):
        for answer_data in data['answers']:
            try:
                question = trip_models.TripQuestion.objects.get(id=answer_data['question_id'])
            except trip_models.TripQuestion.DoesNotExist:
                raise serializers.ValidationError(f"Question {answer_data['question_id']} not found")

            if question.question_type == 'pax':
                if answer_data['answer'] not in dict(trip_models.Trip.TRIP_PAX_TYPE_CHOICES):
                    raise serializers.ValidationError(f"Invalid pax type for question {question.id}")
            elif question.question_type == 'intensity':
                if answer_data['answer'] not in dict(trip_models.Trip.TRIP_INTENSITY_CHOICES):
                    raise serializers.ValidationError(f"Invalid intensity level for question {question.id}")
            elif question.question_type == 'when':
                try:
                    start_date, end_date = answer_data['answer'].split(',')
                    datetime.strptime(start_date.strip(), '%Y-%m-%d')
                    datetime.strptime(end_date.strip(), '%Y-%m-%d')
                except (ValueError, IndexError):
                    raise serializers.ValidationError(f"Invalid date format for question {question.id}. Use YYYY-MM-DD,YYYY-MM-DD")
            elif question.question_type == 'budget':
                try:
                    float(answer_data['answer'])
                except ValueError:
                    raise serializers.ValidationError(f"Budget must be a number for question {question.id}")
            elif question.question_type == 'from':
                # Validate from location if needed
                if not answer_data['answer'].strip():
                    raise serializers.ValidationError("From location cannot be empty")
            elif question.question_type == 'where':
                # Validate destination location if needed
                if not answer_data['answer'].strip():
                    raise serializers.ValidationError("Destination location cannot be empty")

            answer_data['question'] = question

        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        
        # Create new Trip and TripFynder
        trip = trip_models.Trip.objects.create()
        trip_fynder = trip_models.TripFynder.objects.create(
            trip=trip,
            fynder=user
        )

        # Process each answer
        for answer_data in self.validated_data['answers']:
            question = answer_data['question']
            answer = answer_data['answer']

            # Update Trip based on question type
            if question.question_type == 'pax':
                trip.trip_pax_type = answer
            elif question.question_type == 'where':
                trip.location = answer
            elif question.question_type == 'from':
                trip.from_location = answer
            elif question.question_type == 'when':
                start_date, end_date = answer.split(',')
                trip.start_date = start_date.strip()
                trip.end_date = end_date.strip()
            elif question.question_type == 'budget':
                trip.budget = float(answer)
            elif question.question_type == 'intensity':
                trip.trip_intensity = answer

            # Create TripQuestionAnswer
            trip_models.TripFynderAnswer.objects.create(
                trip=trip,
                question=question,
                answer=answer
            )

        trip.save()
        return trip

class AddFriendLinkToTripSerializer(serializers.Serializer):
    trip_id = serializers.CharField()

    def save(self, **kwargs):
        fynder = self.context['request'].user
        trip_id = self.validated_data.get("trip_id")
        if not trip_id:
            raise serializers.ValidationError("Trip ID is required")
        try:
            trip = trip_models.Trip.objects.get(id=trip_id)
        except trip_models.Trip.DoesNotExist:
            raise serializers.ValidationError("Trip not found")
        is_owner = trip_models.TripFynder.objects.filter(trip=trip, fynder=fynder, is_owner=True).exists()
        if is_owner:
            raise serializers.ValidationError("You are the owner of this trip, you cannot add yourself to the trip")
        fynders_already_in_trip = trip_models.TripFynder.objects.filter(trip=trip, fynder=fynder)
        if fynders_already_in_trip.exists():
            for fynder_already_in_trip in fynders_already_in_trip:
                if fynder_models.Friendship.objects.filter(fynder_1=fynder, fynder_2=fynder_already_in_trip.fynder).exists() or fynder_models.Friendship.objects.filter(fynder_1=fynder_already_in_trip.fynder, fynder_2=fynder).exists():
                    pass
                else:
                    fynder_models.Friendship.objects.create(fynder_1=fynder, fynder_2=fynder_already_in_trip.fynder)
        
        trip_fynder = trip_models.TripFynder.objects.create(trip=trip, fynder=fynder)
        return trip
        
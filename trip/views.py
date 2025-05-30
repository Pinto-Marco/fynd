from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter

from trip import models as trip_models
from trip import serializers as trip_serializers
from fynder import serializers as fynder_serializers

# Create your views here.

class TripQuestionListView(APIView):
    serializer_class = trip_serializers.TripQuestionSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: trip_serializers.TripQuestionSerializer(many=True)}
    )
    def get(self, request, format=None):
        questions = trip_models.TripQuestion.objects.all()
        serializer = trip_serializers.TripQuestionSerializer(questions, many=True)
        return Response(serializer.data)

class TripQuestionPaxView(APIView):
    serializer_class = trip_serializers.TripQuestionSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: trip_serializers.TripQuestionSerializer(many=True)}
    )
    def get(self, request, format=None):
        question = trip_models.TripQuestion.objects.filter(question_type="pax").first()
        serializer = trip_serializers.TripQuestionSerializer(question)
        return Response(serializer.data)

class TripQuestionIntesityView(APIView):
    serializer_class = trip_serializers.TripQuestionSerializer
    permission_classes = [IsAuthenticated]
    @extend_schema(
        responses={200: trip_serializers.TripQuestionSerializer(many=True)}
    )
    def get(self, request, format=None):
        question = trip_models.TripQuestion.objects.filter(question_type="intensity").first()
        serializer = trip_serializers.TripQuestionSerializer(question)
        return Response(serializer.data)


class TripFynderAnswerView(APIView):
    serializer_class = trip_serializers.TripFynderAnswerSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["patch"]

    @extend_schema(
        request=trip_serializers.TripFynderAnswerSerializer,
        responses={200: {"message": "Answer updated successfully"}}
    )
    def patch(self, request, question_id, format=None):
        serializer = self.serializer_class(
            data=request.data,
            context={'question_id': question_id, 'request': request}
        )
        
        if serializer.is_valid():
            trip = serializer.save()
            return Response(
                {"id": trip.id },
                status=status.HTTP_200_OK
            )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class TripFynderAnswerAllTogetherView(APIView):
    serializer_class = trip_serializers.TripFynderAnswerAllTogetherSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["post"]
    @extend_schema(
        request=trip_serializers.TripFynderAnswerAllTogetherSerializer,
        responses={200: {"message": "Answers updated successfully"}}
    )
    def post(self, request, format=None):
        serializer = trip_serializers.TripFynderAnswerAllTogetherSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            trip = serializer.save()
            return Response(
                {"id": trip.id },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class AddFriendLinkToTripView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = trip_serializers.AddFriendLinkToTripSerializer
    @extend_schema(
        summary="Add Friend Deep Link To Trip",
        description="Adds a friend with the deep link to trip.",
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
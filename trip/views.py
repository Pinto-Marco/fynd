from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter

from trip import models as trip_models
from trip import serializers as trip_serializers

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

class TripQuestionAnswerView(APIView):
    serializer_class = trip_serializers.TripQuestionAnswerSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["patch"]

    @extend_schema(
        request=trip_serializers.TripQuestionAnswerSerializer,
        responses={200: {"message": "Answer updated successfully"}}
    )
    def patch(self, request, question_id, format=None):
        serializer = self.serializer_class(
            data=request.data,
            context={'question_id': question_id, 'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Answer updated successfully"},
                status=status.HTTP_200_OK
            )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
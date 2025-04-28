from django.urls import path, include
from . import views


urlpatterns = [
    path('question/', views.TripQuestionListView.as_view(), name='trip-question-list'),
    path('question/<int:question_id>', views.TripQuestionAnswerView.as_view(), name='trip-question-answer'),
]
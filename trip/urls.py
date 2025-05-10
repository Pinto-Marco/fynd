from django.urls import path, include
from . import views


urlpatterns = [
    path('question/', views.TripQuestionListView.as_view(), name='trip-question-list'),
    path('question/pax', views.TripQuestionPaxView.as_view(), name='trip-question-list-pax'),
    path('question/intensity', views.TripQuestionIntesityView.as_view(), name='trip-question-list-pax'),
    path('question/<int:question_id>', views.TripFynderAnswerView.as_view(), name='trip-question-answer'), # TODO: remove
    path('question/all-together', views.TripFynderAnswerAllTogetherView.as_view(), name='trip-question-answer-all-together'),
]
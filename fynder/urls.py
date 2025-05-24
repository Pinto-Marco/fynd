from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.CustomRegisterView.as_view(), name='register'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', views.CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.CustomTokenBlacklistView.as_view(), name='token_blacklist'),
    path('delete-data/', views.DeleteDataView.as_view(), name='delete-data'),
    path('delete-account/', views.DeleteAccountView.as_view(), name='delete-account'),
    path("update/", views.UserUpdateView.as_view(), name="user-update"),
    path("profile/", views.UserProfileView.as_view(), name="user-profile"),
    path('request-temporary-code/', views.RequestTemporaryCodeView.as_view(), name='request-temporary-code'),
    path('verify-temporary-code/', views.VerifyTemporaryCodeView.as_view(), name='verify-temporary-code'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path("possible-food-preferences/", views.PossibleFoodPreferencesView.as_view(), name="possible-food-preferences"),
    path('possible-sign-up-question-answer/', views.PossibleSignUpQuestionAnswerView.as_view(), name='possible-sign-up-question-answer'),
    path('fynder-sign-up-question-answer/', views.FynderSignUpQuestionAnswerView.as_view(), name='fynder-sign-up-question-answer'),
    path('profile/friend/', views.AddFriendView.as_view(), name='add-friend'),
    path('profile/friend/link', views.AddFriendLinkView.as_view(), name='add-friend-link'),
    path('profile/friend/<int:friend_id>', views.FriendProfileView.as_view(), name='friend-detail-delete'),
    path('sign-up/basic-cards/', views.SignUpFynderBasicCardsView.as_view(), name='sign-up-basic-cards'),
]

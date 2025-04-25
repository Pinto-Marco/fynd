from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.CustomRegisterView.as_view(), name='register'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', views.CustomTokenRefreshView.as_view(), name='token_refresh'),
    path("update/", views.UserUpdateView.as_view(), name="user-update"),
    path("profile/", views.UserProfileView.as_view(), name="user-profile"),
    path('request-temporary-code/', views.RequestTemporaryCodeView.as_view(), name='request-temporary-code'),
    path('verify-temporary-code/', views.VerifyTemporaryCodeView.as_view(), name='verify-temporary-code'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path("possible-food-preferences/", views.PossibleFoodPreferencesView.as_view(), name="possible-food-preferences"),
]

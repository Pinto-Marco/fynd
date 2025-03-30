from django.urls import path
from .views import CustomRegisterView, CustomTokenObtainPairView, CustomTokenRefreshView, UserUpdateView

urlpatterns = [
    path('register/', CustomRegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path("update/", UserUpdateView.as_view(), name="user-update"),
]

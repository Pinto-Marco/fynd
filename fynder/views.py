from django.core.files.storage import default_storage
from django.conf import settings
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.apple.client import AppleOAuth2Client
from allauth.socialaccount.providers.apple.views import AppleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from dj_rest_auth.registration.views import RegisterView
from drf_spectacular.utils import extend_schema
from . import serializers as fynder_serializers
from rest_framework.response import Response
from rest_framework import status


class CustomAppleOAuth2Client(AppleOAuth2Client):
    def __init__(
            self,
            request,
            consumer_key,
            consumer_secret,
            access_token_method,
            access_token_url,
            callback_url,
            _scope, 
            scope_delimiter=" ",
            headers=None,
            basic_auth=False,
    ):
        super().__init__(
            request,
            consumer_key,
            consumer_secret,
            access_token_method,
            access_token_url,
            callback_url,
            scope_delimiter,
            headers,
            basic_auth,
        )


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.APP_LOGIN_CALLBACK_URL
    client_class = OAuth2Client



class AppleLogin(SocialLoginView):
    adapter_class = AppleOAuth2Adapter
    callback_url = settings.APP_LOGIN_CALLBACK_URL
    client_class = CustomAppleOAuth2Client

User = get_user_model()

class CustomRegisterView(RegisterView):
    serializer_class = fynder_serializers.RegisterSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(summary="User Registration", description="Registers a new user and returns authentication tokens.")
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()  # RIMOSSO `request`
        return Response(fynder_serializers.RegisterSerializer(user).data, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = fynder_serializers.CustomTokenObtainPairSerializer

    @extend_schema(summary="User Login", description="Authenticates a user and returns JWT tokens.")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class CustomTokenRefreshView(TokenRefreshView):
    @extend_schema(summary="Refresh Token", description="Refreshes the access token using the refresh token.")
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)  # Chiama il metodo originale
        refresh = request.data.get("refresh")  # Ottieni il refresh token dalla richiesta
        return Response({
            "access": response.data.get("access"),  
            "refresh": refresh  # Includi anche il refresh token
        })

class UserUpdateView(generics.UpdateAPIView):
    serializer_class = fynder_serializers.UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["put"]

    def get_object(self):
        return self.request.user

    @extend_schema(
        summary="Update User Info",
        description="Updates the user's profile information (excluding password). This PUT method also supports partial updates.",
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

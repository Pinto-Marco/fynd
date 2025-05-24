from re import M
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
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from . import utils as fynder_utils
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import update_session_auth_hash
from . import models as fynder_models
from . import serializers as fynder_serializers


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

class DeleteDataView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @extend_schema(
        summary="Delete User Data",
        description="Deletes the user's data and associated files.",
    )
    def delete(self, request, *args, **kwargs):
        fynder = fynder_models.Fynder(request.user)
        is_delete = fynder.delete_data()
        if is_delete:
            return Response({"message": "User data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "User data not deleted"}, status=status.HTTP_400_BAD_REQUEST)
        
class DeleteAccountView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @extend_schema(
        summary="Delete User Account",
        description="Deletes the user's account and associated files.",
    )
    def delete(self, request, *args, **kwargs):
        fynder = fynder_models.Fynder(request.user)
        is_delete = fynder.delete_data()
        if is_delete:
            fynder.delete()
            return Response({"message": "User account deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "User account not deleted"}, status=status.HTTP_400_BAD_REQUEST)



class UserUpdateView(generics.UpdateAPIView):
    serializer_class = fynder_serializers.UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["patch"]

    def get_object(self):
        return self.request.user

    @extend_schema(
        summary="Update User Info",
        description="Updates the user's profile information (excluding password). This PUT method also supports partial updates.",
    )
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = fynder_serializers.UserUpdateSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return_serializer = fynder_serializers.UserProfileSerializer(instance)
            return Response(return_serializer.data, status=status.HTTP_200_OK)



class RequestTemporaryCodeView(APIView):
    permission_classes = [permissions.AllowAny]
    """
    API endpoint per richiedere un codice temporaneo per il login.
    """
    serializer_class = fynder_serializers.RequestTemporaryCodeSerializer

    def send_email(self, recipient_email, code):
        """
        Invia un'email con il codice temporaneo utilizzando SMTP.
        """
        msg = MIMEMultipart()
        msg["From"] = f"{settings.EMAIL_FROM_NAME} <{settings.EMAIL_USER}>"
        msg["To"] = recipient_email
        msg["Subject"] = "Codice di accesso temporaneo"

        body = f"Il tuo codice temporaneo per accedere è: {code}. Questo codice scade tra 2 minuti."
        msg.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT) as smtp_server:
                smtp_server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
                smtp_server.sendmail(settings.EMAIL_USER, recipient_email, msg.as_string())
            return True
        except Exception as e:
            print(f"Errore nell'invio dell'email: {e}")
            return False

    @extend_schema(
        summary="Request Temporary Code",
        description="Richiede un codice temporaneo per il login e lo invia via email.",
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            try:
                user = fynder_models.Fynder.objects.get(email=email)
            except fynder_models.Fynder.DoesNotExist:
                return Response({"error": "Utente non trovato"}, status=status.HTTP_404_NOT_FOUND)

            # Genera un codice a 6 cifre
            code = fynder_utils.generate_unique_code()

            # Elimina eventuali codici precedenti per lo stesso utente
            fynder_models.TemporaryCode.objects.filter(user=user).delete()

            # Crea un nuovo codice temporaneo
            temp_code = fynder_models.TemporaryCode.objects.create(user=user, code=code)

            # Invia l'email con il codice temporaneo
            if self.send_email(user.email, code):
                return Response({"message": "Codice temporaneo mandato alla tua mail"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Errore nell invio della mail"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class VerifyTemporaryCodeView(APIView):
    """
    API endpoint per verificare il codice temporaneo inviato via email.
    """ 

    permission_classes = [permissions.AllowAny]
    serializer_class = fynder_serializers.VerifyTemporaryCodeSerializer

    
    @extend_schema(
        summary="Verify Temporary Code",
        description="Verifica il codice temporaneo inviato via email e restituisce i token JWT.",
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data["code"]
            try:
                temp_code = fynder_models.TemporaryCode.objects.get(code=code)
            except fynder_models.TemporaryCode.DoesNotExist:
                return Response({"error": "Code invalido o scaduto"}, status=status.HTTP_400_BAD_REQUEST)

            # Verifica che il codice non sia scaduto
            if temp_code.is_expired():
                return Response({"error": "Code scaduto"}, status=status.HTTP_400_BAD_REQUEST)

            # Autenticazione dell'utente
            user = temp_code.user
            # Utilizza il nome utente e la password per fare login
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response({
                'access': access_token,
                'refresh': refresh_token,
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    """
    API endpoint per cambiare la password dell'utente loggato.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = fynder_serializers.ChangePasswordNewSerializer

    @extend_schema(
        summary="Change Password",
        description="Cambia la password dell'utente loggato e restituisce i token JWT.",
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data["new_password"]
            user = request.user

            # Imposta la nuova password
            user.set_password(new_password)
            user.save()

            # Rilascia i nuovi token
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # Aggiorna la sessione
            update_session_auth_hash(request, user)

            return Response({
                'access': access_token,
                'refresh': refresh_token,
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveAPIView):
    serializer_class = fynder_serializers.UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self):
        return self.request.user
    @extend_schema(
        summary="User Profile",
        description="Retrieves the user's profile information. Includes food preferences which is a list of strings.",
    )
    def get(self, request, *args, **kwargs):

        return self.retrieve(request, *args, **kwargs)

class PossibleFoodPreferencesView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = fynder_serializers.AllPossibleFoodPreferencesSerializer
    
    @extend_schema(
        summary="Possible Food Preferences",
        description="Retrieves a list of possible food preferences.",
    )
    def get(self, request, *args, **kwargs):
        food_preferences = [choice[0] for choice in fynder_models.FynderFoodPreference.FOOD_PREFERENCE_CHOICES]
        return Response({"food_preferences": food_preferences}, status=status.HTTP_200_OK)
    
class PossibleSignUpQuestionAnswerView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = fynder_serializers.PossibleSignUpQuestionAnswerSerializer

    @extend_schema(
        summary="Possible Question Answer",
        description="Retrieves a list of possible questions and answers.",
    )
    def get(self, request, *args, **kwargs):
        questions = fynder_models.SignUpQuestion.objects.all()
        serializer = self.serializer_class(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FynderSignUpQuestionAnswerView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = fynder_serializers.SignUpFynderAnswerSerializer

    @extend_schema(
        summary="Sign Up Question Answer",
        description="Creates or updates a question answer for the logged-in user.",
        request=fynder_serializers.SignUpFynderAnswerSerializer(many=True),
        responses={201: fynder_serializers.SignUpFynderAnswerSerializer(many=True)}
    )
    def post(self, request, *args, **kwargs):
        fynder = request.user
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save(fynder=fynder)
            fynder = fynder.set_calculate_interest()
            return_serializer = fynder_serializers.UserProfileSerializer(fynder)
            return Response(return_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Get Sign Up Question Answer",
        description="Retrieves a list of question answers for the logged-in user.",
        responses={200: fynder_serializers.GetSignUpFynderAnswerSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        fynder = request.user
        answers = fynder_models.SignUpFynderAnswer.objects.filter(fynder=fynder).order_by('answer__question__id').distinct('answer__question__id')
        serializer = fynder_serializers.GetSignUpFynderAnswerSerializer(answers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
class FriendProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = fynder_serializers.UserProfileSerializer
    @extend_schema(
        summary="Friend Profile",
        description="Retrieves the profile of a friend.",
    )
    def get(self, request, friend_id):
        # Ottieni l'ID dell'utente corrente
        user_id = request.user.id
        # Verifica se l'utente corrente è un amico dell'utente specificato
        friendship = fynder_models.Friendship.objects.filter(
            models.Q(fynder_1=request.user, friend_2_id=friend_id) |
            models.Q(fynder_1_id=friend_id, friend_2=request.user)
        ).first()
        if not friendship:
            return Response({"detail": "Non sei un amico di questo utente."}, status=status.HTTP_403_FORBIDDEN)

        # Get friend from friendship
        friend = friendship.friend_2 if friendship.fynder_1 == request.user else friendship.fynder_1
        serializer = self.serializer_class(friend)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AddFriendView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(
        summary="Add Friend",
        description="Adds a friend to the logged-in user's friend list.",
    )
    def post(self, request, friend_id):
        # Ottieni l'ID dell'utente corrente
        user_id = request.user.id
        # Verifica se l'utente corrente è già un amico dell'utente specificato
        if user_id == friend_id:
            return Response({"detail": "Non puoi aggiungerti come amico."}, status=status.HTTP_400_BAD_REQUEST)
        friendship = fynder_models.Friendship.objects.filter(
            models.Q(fynder_1=request.user, friend_2_id=friend_id) |
            models.Q(fynder_1_id=friend_id, friend_2=request.user)
        ).first()
        if friendship:
            return Response({"detail": "Sei già un amico di questo utente."}, status=status.HTTP_400_BAD_REQUEST)
        # Crea una nuova relazione di amicizia
        new_friendship = fynder_models.Friendship.objects.create(fynder_1=request.user, friend_2_id=friend_id)
        return Response({"detail": "Amicizia aggiunta con successo."}, status=status.HTTP_201_CREATED)

    # delete friendship
    @extend_schema(
        summary="Remove Friend",
        description="Removes a friend from the logged-in user's friend list.",
    )
    def delete(self, request, friend_id):
        # Ottieni l'ID dell'utente corrente
        user_id = request.user.id
        # Verifica se l'utente corrente è già un amico dell'utente specificato
        friendship = fynder_models.Friendship.objects.filter(
            models.Q(fynder_1=request.user, friend_2_id=friend_id) |
            models.Q(fynder_1_id=friend_id, friend_2=request.user)
        ).first()
        if not friendship:
            return Response({"detail": "Non sei un amico di questo utente."}, status=status.HTTP_400_BAD_REQUEST)
        # Elimina la relazione di amicizia
        friendship.delete()
        return Response({"detail": "Amicizia rimossa con successo."}, status=status.HTTP_200_OK)

class AddFriendLinkView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = fynder_serializers.AddFriendLinkSerializer
    @extend_schema(
        summary="Add Friend Deep Link",
        description="Adds a friend with the deep link.",
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class CustomTokenBlacklistView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Logout",
        description="Blacklists the refresh token, effectively logging out the user",
        request={
            'application/json': {
                'type': 'object',
                'required': ['refresh'],
                'properties': {
                    'refresh': {
                        'type': 'string',
                        'description': 'The refresh token to blacklist'
                    }
                }
            }
        },
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'Successfully logged out'
                    }
                }
            },
            400: {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'example': 'Invalid token'
                    }
                }
            }
        }
    )
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    {"error": "Refresh token is required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response(
                {"message": "Successfully logged out"}, 
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": "Invalid token"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

class SignUpFynderBasicCardsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = fynder_serializers.SignUpFynderBasicCardsSerializer
    @extend_schema(
        # la request è una lista di id 
        request=fynder_serializers.SignUpFynderBasicCardsSerializer(many=True),
        summary="Sign Up Basic Cards",
        description="Adds basic cards to the logged-in user's basic cards list.",
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
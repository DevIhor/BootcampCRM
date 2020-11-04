from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenVerifySerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView, TokenRefreshView

from apps.authentication.serializers import CustomTokenObtainPairSerializer, SignUpSerializer, ActivationTokenSerializer


class ObtainJSONWebToken(TokenObtainPairView):
    """
    post:
    Generate REST API token.
    Generate personal REST API token with expired date `ACCESS_TOKEN_LIFETIME_HOURS` or/and
    `ACCESS_TOKEN_LIFETIME_MINUTES`.
    In a few words - it's an authentication token. To work with API you need to have it, entering your email
    and password. Each time you request to the API, you need to send in header your token like
    `Authorization: JWT eyJ0eXAiOiJKV...`, where `JWT` is header authorization prefix.
    ### Examples
    If data is successfully processed the server returns status code `200`.
    ```json
    {
        "email": "watch.dog@coaxsoft.com",
        "password": "qwerty123"
    }
    ```
    ### Errors
    If there were some error in client data, it sends status code `401` with the error message looks like:
    ```json
    {
        "detail": "No active account found with the given credentials"
    }
    ```
    """
    serializer_class = CustomTokenObtainPairSerializer


class VerifyJSONWebToken(TokenVerifyView):
    """
    post:
    Verify your token (is it valid?)
    To work with API you need to have valid (verified) token which you get after visiting `/auth/verify` url, entering
    your token.[Read JWT docs](https://jwt.io/)
    ### Examples
    If data is successfully processed the server returns status code `200`.
    ```json
    {
        "token": "khgkjwehrgjkher8356khjhgjhvjhb345j54bjkbj45"
    }
    ```
    ### Errors
    If there were some error in client data, it sends status code `401` with the error message looks like:
    ```json
    {
        "detail": "Token is invalid or expired",
        "code": "token_not_valid"
    }
    ```
    """
    serializer_class = TokenVerifySerializer


class RefreshJSONWebToken(TokenRefreshView):
    """
    post:
    Refresh expired JSON Web Token.
    It is used JWT authentication with refresh expiration time = 14 days [Read JWT docs](https://jwt.io/). It means,
    that you have 14 days, from the time your token was generated, to update token with new one. You need to send your
    JSON WEB Token.
    ### Examples
    If data is successfully processed the server returns status code `200`.
    ```json
    {
        "refresh": "khgkjwehrgjkher8356khjhgjhvjhb345j54bjkbj45"
    }
    ```
    ### Errors
    If there were some error in client data, it sends status code `401` with the error message looks like:
    ```json
    {
        "detail": "Token is invalid or expired",
        "code": "token_not_valid"
    }
    ```
    """
    serializer_class = TokenRefreshSerializer


class SignUpView(CreateAPIView):
    """
    Register new user in the system
    You need to provide `email`, `first_name`, `last_name`, `password_repeated`
    """
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer


class ActivateUserView(APIView):
    """
    Activate user account
    """
    serializer_class = ActivationTokenSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=ActivationTokenSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.activate_user()
            email = force_text(urlsafe_base64_decode(serializer.validated_data['token'].split('.')[0]))
            user = User.objects.get(email=email)
            token = RefreshToken.for_user(user)
            return Response(data={'access_token': str(token.access_token), 'refresh_token': str(token)}, status=200)
        return Response(status=404)

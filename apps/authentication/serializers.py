import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.authentication.utils import TokenGenerator

logger = logging.getLogger("main")


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Obtain token when doing log in
    """
    default_error_messages = {'no_active_account': 'Incorrect username or password'}

    def validate(self, attrs):
        attrs['email'] = attrs['email'].lower()
        data = super().validate(attrs)
        self.user.last_login_date = timezone.now()
        self.user.save(update_fields=('last_login_date', ))
        logger.info(f"User {self.user.username} was successfully logged in")
        return data


class SignUpSerializer(ModelSerializer):
    """
    Create new user when doing sign up
    """
    password_repeated = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    url = serializers.RegexField(regex=r'[a-zA-Z0-9_\-\/]+', required=True, write_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "password", "password_repeated", "role", "url")
        read_only_fields = ("id", "role")
        write_only_fields = ("password", "password_repeated", "url")

    def validate(self, data):
        if data['password_repeated'] != data['password']:
            error = "Repeated password is not equal to password"
            raise serializers.ValidationError(error)
        return data

    def validate_email(self, value):
        if User.objects.filter(email=value, is_active=True).exists():
            error = f"User with the email '{value}' already exists"
            raise serializers.ValidationError(error)
        return value.lower()

    def create(self, validated_data, is_dealer=False):
        validated_data.pop('password_repeated')
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        if validated_data.get('role'):
            user.role = validated_data['role']
        user.set_password(validated_data['password'])
        user.save()

        token = f"{urlsafe_base64_encode(force_bytes(user.email))}.{TokenGenerator.make_token(user)}"

        if is_dealer:
            template = 'notifications/activation_email_dealer.html'
        else:
            template = 'notifications/activation_email.html'

        url = validated_data.pop('url', '')
        url = create_url(url, token)
        send_email.delay(
            subject="Welcome to Bootcamp CRM",
            template=template,
            recipients=[user.email],
            context={
                'url': url,
                'email': user.email,
                'contact': settings.BCRM_INFO_PHONE
            })

        return user


class ActivationTokenSerializer(serializers.Serializer):
    """
    Activate user when doing activation through email
    """
    token = serializers.CharField()

    def validate(self, data):
        token = data['token']
        error = f"Provided activation token '{token}' is not valid"
        try:
            uid, token = token.split('.')
            uid = force_text(urlsafe_base64_decode(uid))
        except (TypeError, ValueError):
            raise serializers.ValidationError(error)

        try:
            user = User.objects.get(email=uid)
        except User.DoesNotExist:
            raise serializers.ValidationError(error)

        if not TokenGenerator.check_token(user, token):
            raise serializers.ValidationError(error)

        data['email'] = uid
        return data

    def activate_user(self):
        user = User.objects.get(email=self.validated_data['email'])
        user.is_active = True
        user.confirmation = ConfirmationChoices.CONFIRMED.name
        user.save()

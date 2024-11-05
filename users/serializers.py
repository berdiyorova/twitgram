import re

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from users.models import UserModel


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(validators=[UniqueValidator(
        queryset=UserModel.objects.all(),
        message="This email is already registered")
    ])

    class Meta:
        model = UserModel
        fields = ('username', 'email', 'password', 'confirm_password')

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        # validate password
        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")

        try:
            validate_password(password=password)  # validate_password
        except Exception as e:
            raise serializers.ValidationError(str(e))

        # validate email
        pattern = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b")

        if not re.match(pattern, email):
            raise ValidationError('Invalid email format.')
        if not email.endswith('@gmail.com'):
            raise ValidationError("Email must end with '@gmail.com'.")

        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = UserModel.objects.create(**validated_data)

        user.set_password(validated_data['password'])
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)

import threading
from datetime import datetime

from django.contrib.auth import authenticate
from django.core.mail import send_mail
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from Config.settings import EMAIL_HOST_USER
from users.models import UserModel
from users.serializers import RegisterSerializer, LoginSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = UserModel.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        user.is_staff = False
        user.save()

        return Response({
            'success': True,
            'message': f"Verification code sent to {user.email}.",
        }, status=status.HTTP_201_CREATED)


class VerifyView(APIView):

    def post(self, *args, **kwargs):
        email = self.request.data.get('email')
        code = self.request.data.get('code')
        user = UserModel.objects.get(email=email)

        self.check_verify(user, code)
        return Response(
            data={
                'success': True,
                'message': 'Your email has been verified.'
            }, status=status.HTTP_200_OK
        )

    @staticmethod
    def check_verify(user, code):
        verifies = user.verify_codes.filter(expiration_time__gte=datetime.now(), code=code, is_confirmed=False)
        if not verifies.exists():
            data = {
                'message': 'Your verification code is incorrect or out of date.'
            }
            raise ValidationError(data)
        else:
            verifies.update(is_confirmed=True)

        return True


class ResendVerifyView(APIView):
    def post(self, *args, **kwargs):
        email = self.request.data.get('email')
        user = UserModel.objects.get(email=email)
        code = user.create_verify_code()
        subject = "Welcome to TwitGram!"
        message = f"Hi, {user.username}, Your verification code is: {code}."

        t = threading.Thread(target=send_mail, args=(subject, message, EMAIL_HOST_USER, [email]))
        t.start()

        return Response(
            data={
                'success': True,
                'message': 'Your email has been verified.'
            }, status=status.HTTP_200_OK
        )


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)

            response = {
                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token),
            }
            return Response(response, status=status.HTTP_200_OK)

        return Response({
            'success': False,
            'message': 'Invalid credentials'
        }, status=status.HTTP_400_BAD_REQUEST)

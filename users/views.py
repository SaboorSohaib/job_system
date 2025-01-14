# users/views.py
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from .models import OTP
from .serializers import RegisterSerializer, OTPSerializer, LoginSerializer
from django.core.mail import send_mail
from django.conf import settings
import random
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth import login

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    authentication_classes = []
    permission_classes = []
    
    def perform_create(self, serializer):
        user = serializer.save()
        # Generate OTP
        otp_code = str(random.randint(100000, 999999))
        otp = OTP.objects.create(user=user, otp_code=otp_code)
        
        # Send OTP to user's email
        send_mail(
            'Your OTP code',
            f'Your OTP code is {otp_code}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return Response({'message': 'User created. Please verify your email.'}, status=status.HTTP_201_CREATED)


class VerifyEmailView(APIView):
    serializer_class = OTPSerializer
    authentication_classes = []
    permission_classes = []
    
    def post(self, request):
        otp_code = request.data.get('otp_code')

        # Check if OTP code is provided
        if not otp_code:
            return Response(
                {'error': 'OTP code is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Retrieve the OTP object based on the code
            otp = OTP.objects.get(otp_code=otp_code, is_used=False)
            user = otp.user

            # Check if the user's email is already verified
            if user.is_email_verified:
                return Response(
                    {'message': 'Email is already verified. You can log in.'},
                    status=status.HTTP_200_OK
                )

            # If email is not verified, proceed with OTP verification
            otp.is_used = True  # Mark OTP as used
            otp.save()

            user.is_email_verified = True  # Mark user email as verified
            user.save()
            send_mail(
            'Email Verified',
            f'Your email is verified',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
            return Response(
                {'message': 'Email verified successfully!'},
                status=status.HTTP_200_OK
            )

        except OTP.DoesNotExist:
            return Response(
                {'error': 'Invalid or expired OTP.'},
                status=status.HTTP_400_BAD_REQUEST
            )


class LoginView(APIView):
    serializer_class = LoginSerializer
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            access_token = AccessToken.for_user(user)

            request.session['access_token'] = str(access_token)
            request.session.save()

            return Response({
                'message': 'User logged in successfully.',
                'access_token': str(access_token), 
            }, status=status.HTTP_200_OK)
        
        return Response({
            'error': 'Invalid username or password.',
        }, status=status.HTTP_400_BAD_REQUEST)

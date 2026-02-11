from rest_framework.views import APIView
from authentication.serializers import SignupSerializer
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import authenticate
import random
from authentication.models import OTP

from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.core.mail import send_mail


# Create your views here.

class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # 1. Verify credentials
        user = authenticate(username=username, password=password)

        if user is not None:
            # 2. Generate a random 6-digit code
            otp_code = str(random.randint(100000, 999999))

            # 3. Save OTP to database (overwrite if one already exists for this user)
            OTP.objects.update_or_create(user=user, defaults={'code': otp_code})

            # # 4. Print to Terminal (Instead of sending email)
            # print("\n" + "=" * 30)
            # print(f"DEBUG OTP FOR {username}: {otp_code}")
            # print("=" * 30 + "\n")

            # --- UPDATED: SEND ACTUAL EMAIL ---
            subject = 'Your Verification Code'
            message = f'Hello {user.username},\n\nYour 6-digit verification code is: {otp_code}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email]

            try:
                send_mail(subject, message, email_from, recipient_list)
            except Exception as e:
                return Response({"error": "Failed to send email. Check SMTP settings."},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({
                "message": f"Login successful. OTP has been sent to {user.email}."
            }, status=status.HTTP_200_OK)

        return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)

class VerifyOTPView(APIView):
    def post(self, request):
        username = request.data.get('username')
        otp_code = request.data.get('otp')

        try:
            # 1. Find the OTP record for this user
            otp_record = OTP.objects.get(user__username=username, code=otp_code)

            # 2. If found, generate JWT tokens
            user = otp_record.user
            refresh = RefreshToken.for_user(user)

            # 3. Delete the OTP so it can't be used again
            otp_record.delete()

            return Response({
                "message": "OTP Verified successfully!",
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)

        except OTP.DoesNotExist:
            return Response({
                "error": "Invalid OTP or Username"
            }, status=status.HTTP_400_BAD_REQUEST)

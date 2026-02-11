from django.urls import path
from authentication.views import SignupView, LoginView, VerifyOTPView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
]
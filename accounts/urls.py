from django.urls import path
from .views import (
    RegisterView,LoginView,AccountVerifiedTokenView,ResendAccountVerifiedTokenView,
    LogoutView,ProfileView,ProfileUpdateView,ChangePasswordTokenView,ChangePasswordView,
    ForgotPasswordTokenView,ForgotPasswordView
)

urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('account_verified/<uuid:token>/',AccountVerifiedTokenView.as_view(),name='account_verified_token'),
    path('resend_account_token/',ResendAccountVerifiedTokenView.as_view(),name='resend_account_token'),
    path('Logout/',LogoutView.as_view(),name='logout'),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('profile/update/',ProfileUpdateView.as_view(),name='profile_update'),
    path('change_password_token/',ChangePasswordTokenView.as_view(),name='change_password_token'),
    path('change_password/<uuid:token>/',ChangePasswordView.as_view(),name='change_password'),
    path('forgot_password_token/',ForgotPasswordTokenView.as_view(),name='forgot_password_token'),
    path('forgot_password/<uuid:token>/',ForgotPasswordView.as_view(),name='forgot_password')
]
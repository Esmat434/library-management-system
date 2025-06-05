from django.urls import path
from .views import (
    RegisterView,LoginView,AccountVerifiedTokenView,AccountVerifiedResendTokenView,
    LogoutView,ProfileView,ProfileUpdateView,ChangePasswordTokenView,ChangePasswordView,
    ForgotPasswordResendLinkView,ForgotPasswordView
)

app_name = 'accounts'

urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('account_verified/<uuid:token>/',AccountVerifiedTokenView.as_view(),name='account_verified_token'),
    path('account_resend_token/',AccountVerifiedResendTokenView.as_view(),name='account_resend_token'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('profile/update/',ProfileUpdateView.as_view(),name='profile_update'),
    path('change_password_token/',ChangePasswordTokenView.as_view(),name='change_password_token'),
    path('change_password/<uuid:token>/',ChangePasswordView.as_view(),name='change_password'),
    path('forgot_password_token/',ForgotPasswordResendLinkView.as_view(),name='forgot_password_resend_token'),
    path('forgot_password/<uuid:token>/',ForgotPasswordView.as_view(),name='forgot_password')
]
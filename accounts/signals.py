from django.urls import reverse
from django.contrib.auth.signals import user_login_failed
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from django.conf import settings
import time

from .email_config import send_verification_mail

from .models import (
    CustomUser,AccountVerificationToken,ChangePasswordToken,ForgotPasswordToken
)

@receiver(post_save,sender = CustomUser)
def create_account_verify_token(sender,created,instance,**kwargs):
    if created:
        AccountVerificationToken.objects.create(user = instance)

@receiver(post_save,sender = AccountVerificationToken)
def send_email_account_verification_token(sender,created,instance,**kwargs):
    domain = getattr(settings,'SITE_DOMAIN','http://localhost:8000')
    url = domain + reverse('accounts:account_verified_token',args=[instance.token])
    send_verification_mail(instance.user.email,'Account Verification Link',instance.user.username,url)

@receiver(post_save,sender = ChangePasswordToken)
def send_email_change_password_token(sender,created,instance,**kwargs):
    domain = getattr(settings,'SITE_DOMAIN','http://localhost:8000')
    url = domain + reverse('accounts:change_password',args=[instance.token])
    send_verification_mail(instance.user.email,'Change Password Verification Link',instance.user.username,url)

@receiver(post_save,sender = ForgotPasswordToken)
def send_email_forgot_password_token(sender,created,instance,**kwargs):
    domain = getattr(settings,'SITE_DOMAIN','http://localhost:8000')
    url = domain + reverse('accounts:forgot_password',args=[instance.token])
    send_verification_mail(instance.user.email,'Forgot Password Verification Link',instance.user.username,url)

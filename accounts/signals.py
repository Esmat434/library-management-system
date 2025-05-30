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
    
    send_verification_mail(instance.user.email,'Account Verification Link',instance.token)

@receiver(post_save,sender = ChangePasswordToken)
def send_email_change_password_token(sender,created,instance,**kwargs):
    
    send_verification_mail(instance.user.email,'Change Password Verification Link',instance.token)

@receiver(post_save,sender = ForgotPasswordToken)
def send_email_forgot_password_token(sender,created,instance,**kwargs):
    
    send_verification_mail(instance.user.email,'Forgot Password Verification Link',instance.token)

def get_client_ip_from_request(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@receiver(user_login_failed)
def user_login_failed_receiver(sender,credentials,request,**kwargs):
    if not request:
        return
    
    ip_address = get_client_ip_from_request(request)
    username = credentials.get('username')

    if not username:
        return 
    
    attempt_count_key = f'login_attempts_{ip_address}_{username}'
    lockout_cache_key = f'lockout_{ip_address}_{username}'
    lockout_remaining_time_key = f'lockout_expiry_{ip_address}_{username}'

    attempts = cache.get(attempt_count_key,0)+1

    if attempts >= settings.MAX_LOGIN_ATTEMPTS:
        
        cache.set(lockout_cache_key, True, settings.LOGIN_ATTEMPT_LOCKOUT_TIME)
        cache.set(lockout_remaining_time_key, time.time() + settings.LOGIN_ATTEMPT_LOCKOUT_TIME, settings.LOGIN_ATTEMPT_LOCKOUT_TIME)
        
        cache.delete(attempt_count_key)
    else:
        cache.set(attempt_count_key, attempts, settings.LOGIN_ATTEMPT_LOCKOUT_TIME * 2) 

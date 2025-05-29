from django.db.models.signals import post_save
from django.dispatch import receiver

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

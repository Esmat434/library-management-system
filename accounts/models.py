from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from uuid import uuid4
from django.utils import timezone

class CustomUser(AbstractUser):
    CHOICE_ROLE = [
        ('admin','admin'),
        ('librarian','librarian'),
        ('user','user')
    ]
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to=('user/profile_image'))
    passport = models.ImageField(upload_to=('user/passport_image'))
    phone_number = models.CharField(max_length=150)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = CountryField()
    role = models.CharField(max_length=50,default='user',choices=CHOICE_ROLE)
    birth_date = models.DateField()
    email_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username

class TokenBaseClass(models.Model):
    def get_default_token_expiration():
        return timezone.now() + timedelta(hours=24)
    
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=get_default_token_expiration)

    class Meta:
        abstract = True

    def __str__(self):
        return f"This token fro {self.user.username}"
    
    def is_expired(self):
        return timezone.now() >= self.expires_at

class AccountVerificationToken(TokenBaseClass):
    token = models.UUIDField(default=uuid4)

class ChangePasswordToken(TokenBaseClass):
    token = models.UUIDField(default=uuid4)
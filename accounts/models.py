from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField

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
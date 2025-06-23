from django.contrib import admin

from .models import (
    Contact
)
# Register your models here.

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['user','title','username','email','phone_number']
    list_filter = ['title','user','username']
    search_fields = ['title','username','email']
    
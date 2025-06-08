from django.contrib import admin

from .models import (
    Book,Category,Author,Publisher,BookCopy,BorrowTransaction,Reservation,Fine,
)
# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id','title','category','author','publisher','isbn','total_copies','available_copies','published_date']
    list_filter = ['category','author','publisher']
    search_fields = ['id','title','isbn']
    ordering = ['-id']

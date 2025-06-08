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

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    search_fields = ['id','name']
    ordering = ['id']

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id','username','email','first_name','last_name','age','address']
    list_filter = ['first_name','last_name','age','address']
    search_fields = ['id','username','email']
    ordering = ['id']

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ['id','username','email','first_name','last_name','age','address']
    list_filter = ['first_name','last_name','age','address']
    search_fields = ['id','username','email']
    ordering = ['id']

@admin.register(BookCopy)
class BookCopyAdmin(admin.ModelAdmin):
    list_display = ['id','book','copy_number','status','location','created_at']
    list_filter = ['status','location']
    search_fields = ['id','copy_number']
    ordering = ['id']

@admin.register(BorrowTransaction)
class BorrowTransactionAdmin(admin.ModelAdmin):
    list_display = ['id','user','book_copy','is_returned','due_date','return_date']
    list_filter = ['is_returned']
    search_fields = ['id']
    ordering = ['id']

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['id','user','book','is_active','reservation_date']
    list_filter = ['is_active','reservation_date']
    search_fields = ['id']
    ordering = ['id']

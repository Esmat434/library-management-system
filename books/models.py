from django.db import models

# Create your models here.

class Book(models.Model):
    author = models.ForeignKey('Author', on_delete=models.PROTECT)
    publisher = models.ForeignKey('Publisher', on_delete=models.PROTECT)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    
    title = models.CharField(max_length=150)
    description = models.TextField()
    isbn = models.CharField(max_length=13,unique=True)
    
    total_copies = models.IntegerField(default=0)
    available_copies  = models.IntegerField(default=0)
    
    published_date = models.DateField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=155)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class BaseInfo(models.Model):
    username = models.CharField(max_length=155)
    email = models.EmailField()
    first_name = models.CharField(max_length=155,blank=True)
    last_name = models.CharField(max_length=155,blank=True)
    age = models.PositiveIntegerField(default=0)
    address = models.CharField(max_length=255,blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.username

class Author(BaseInfo):
    ...
 
class Publisher(BaseInfo):
    ...

class BookCopy(models.Model):
    Book_Status = (
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('reserved', 'Reserved'),
        ('lost', 'Lost')
    )

    book = models.ForeignKey(Book,on_delete=models.PROTECT)
    copy_number = models.IntegerField(default=0)
    status = models.CharField(max_length=20,choices=Book_Status,default='available')
    location = models.CharField(max_length=155)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['book','copy_number'],name='unique_book_copy'),
            models.CheckConstraint(check=models.Q(copy_number__gte=0),name='copy_number_non_negative')
        ]

    def __str__(self):
        return f"copy from {self.book.title}"
    
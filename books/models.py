from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Book(models.Model):
    author = models.ForeignKey('Author', on_delete=models.PROTECT,related_name='books')
    publisher = models.ForeignKey('Publisher', on_delete=models.PROTECT,related_name='books')
    category = models.ForeignKey('Category', on_delete=models.PROTECT,related_name='books')
    
    title = models.CharField(max_length=150,unique=True)
    description = models.TextField()
    isbn = models.CharField(max_length=13,unique=True)
    slug = models.CharField(max_length=150,unique=True)
    avatar = models.ImageField(upload_to='book/')
    
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
    username = models.CharField(max_length=155,unique=True)
    email = models.EmailField(unique=True)
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

    book = models.ForeignKey(Book,on_delete=models.PROTECT,related_name='book_copy')
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
    
class BorrowTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT,related_name='borrow_transaction')
    book_copy = models.ForeignKey(BookCopy, on_delete=models.PROTECT,related_name='borrow_transaction')
    fine_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    is_returned = models.BooleanField(default=False)
    due_date = models.DateField()
    return_date = models.DateField(blank=True,null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user','book_copy'],name='unique_borrow_transaction')
        ]
    
    def __str__(self):
        return f"borrow {self.book_copy.book.title} to {self.user.username}"
    
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservation')
    book_copy = models.ForeignKey(BookCopy, on_delete=models.PROTECT, related_name='reservation')
    is_active = models.BooleanField(default=False)
    reservation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user','book_copy'],name='unique_reservation')
        ]
    
    def __str__(self):
        return f"{self.user.username} reserved {self.book_copy.book.title}"

class Fine(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='fine')
    borrow_transaction = models.ForeignKey(BorrowTransaction, on_delete=models.PROTECT, related_name='borrow_transaction')
    amount = models.DecimalField(max_digits=8,decimal_places=2)
    is_paid = models.BooleanField(default=False)
    payment_date = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user','borrow_transaction'],name='unique_fine')
        ]

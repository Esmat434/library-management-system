from django.test import TestCase
from django.contrib.auth import get_user_model

from books.models import (
    Book,Author,Category,Publisher,BookCopy,BorrowTransaction,Reservation
)

User=get_user_model()

class TestSendBorrowTransactionNotificationSignal(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test', email='test@gmail.com', avatar='', passport='', 
            address='test', city='test', country='AF', birth_date='2020-01-02', email_verified=True,
            password='Test12345%'
        )
        
        self.category = Category.objects.create(name='test_category')
        
        self.author = Author.objects.create(username='test', email='test@gmail.com', age=20)
        
        self.publisher = Publisher.objects.create(username='test', email='test@gmail.com', age=20)
        
        self.book = Book.objects.create(
            author=self.author, publisher=self.publisher, category=self.category,
            title='test', description='test description', isbn='123', slug='test',
            avatar='', total_copies=10, available_copies=10, published_date='2025-06-11'
        )

        self.book_copy = BookCopy.objects.create(
            book=self.book, copy_number=2, location='test'
        )

    def test_send_borrow_transaction_notification(self):
        self.borrow_transaction = BorrowTransaction.objects.create(
            user=self.user, book_copy=self.book_copy, due_date='2025-06-11'
        )

class TestSendReservedNotificationSignal(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test', email='test@gmail.com', avatar='', passport='', 
            address='test', city='test', country='AF', birth_date='2020-01-02', email_verified=True,
            password='Test12345%'
        )
        
        self.category = Category.objects.create(name='test_category')
        
        self.author = Author.objects.create(username='test', email='test@gmail.com', age=20)
        
        self.publisher = Publisher.objects.create(username='test', email='test@gmail.com', age=20)
        
        self.book = Book.objects.create(
            author=self.author, publisher=self.publisher, category=self.category,
            title='test', description='test description', isbn='123', slug='test',
            avatar='', total_copies=10, available_copies=10, published_date='2025-06-11'
        )

        self.book_copy = BookCopy.objects.create(
            book=self.book, copy_number=2, location='test'
        )
    
    def test_send_reserved_notification(self):
        self.reservation = Reservation.objects.create(
            user=self.user, book_copy=self.book_copy
        )
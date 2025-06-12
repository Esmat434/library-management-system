from django.test import TestCase
from django.contrib.auth import get_user_model

from books.models import (
    Book,Author,Publisher,Category,BookCopy,BorrowTransaction,Reservation,Fine
)

User=get_user_model()

class TestBookModel(TestCase):
    
    def setUp(self):
        self.category = Category.objects.create(name='test_category')
        
        self.author = Author.objects.create(username='test', email='test@gmail.com', age=20)
        
        self.publisher = Publisher.objects.create(username='test', email='test@gmail.com', age=20)
        
        self.book = Book.objects.create(
            author=self.author, publisher=self.publisher, category=self.category,
            title='test', description='test description', isbn='123', slug='test',
            avatar='', total_copies=10, available_copies=10, published_date='2025-06-11'
        )
    
    def test_book_validate_data(self):
        self.assertEqual(self.book.title,'test')
        self.assertEqual(self.book.category,self.category)
        self.assertEqual(self.book.isbn,'123')

class TestCategoryModel(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='test'
        )
    
    def test_category_validate_data(self):
        self.assertEqual(self.category.name,'test')

class TestAuthorModel(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            username='test', email='test@gmail.com',first_name='test', last_name='test', age=20,
            address='test'
        )
    
    def test_author_validate_data(self):
        self.assertEqual(self.author.username,'test')
        self.assertEqual(self.author.email,'test@gmail.com')
        self.assertEqual(self.author.age,20)

class TestPublisherModel(TestCase):
    def setUp(self):
        self.publisher = Publisher.objects.create(
            username='test', email='test@gmail.com',first_name='test', last_name='test', age=20,
            address='test'
        )
    
    def test_author_validate_data(self):
        self.assertEqual(self.publisher.username,'test')
        self.assertEqual(self.publisher.email,'test@gmail.com')
        self.assertEqual(self.publisher.age,20)

class TestBookCopyModel(TestCase):
    def setUp(self):
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
    
    def test_book_copy_validate_data(self):
        self.assertEqual(self.book_copy.book,self.book)
        self.assertEqual(self.book_copy.copy_number,2)
        self.assertEqual(self.book_copy.location,'test')

class TestBorrowTransactionModel(TestCase):
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

        self.borrow_transaction = BorrowTransaction.objects.create(
            user=self.user, book_copy=self.book_copy, due_date='2025-06-11'
        )
    
    def test_borrow_transaction_validate_data(self):
        self.assertEqual(self.borrow_transaction.user,self.user)
        self.assertEqual(self.borrow_transaction.book_copy,self.book_copy)
        self.assertEqual(self.borrow_transaction.due_date,'2025-06-11')

class TestReservationModel(TestCase):
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

        self.reservation = Reservation.objects.create(
            user=self.user, book_copy=self.book_copy
        )
    
    def test_reservation_validate_data(self):
        self.assertEqual(self.reservation.user,self.user)
        self.assertEqual(self.reservation.book_copy,self.book_copy)

class TestFineModel(TestCase):
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

        self.borrow_transaction = BorrowTransaction.objects.create(
            user=self.user, book_copy=self.book_copy, due_date='2025-06-11'
        )

        self.fine = Fine.objects.create(
            user=self.user, borrow_transaction=self.borrow_transaction, amount=0.0, is_paid=True
        )
    
    def test_fine_validate_data(self):
        self.assertEqual(self.fine.user,self.user)
        self.assertEqual(self.fine.borrow_transaction,self.borrow_transaction)
        self.assertEqual(self.fine.amount,0.0)
        self.assertEqual(self.fine.is_paid,True)
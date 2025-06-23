from django.test import TestCase,Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from books.models import (
    Book,Author,Publisher,Category,BookCopy,BorrowTransaction
)

User = get_user_model()

class TestBookListView(TestCase):
    def setUp(self):
        self.url = reverse('books:home')

    def test_get_book_list_validate(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response,'books/book_list.html')
        self.assertEqual(response.status_code,200)

        self.assertEqual(len(response.context['books']),0)
        self.assertIn('books',response.context)

class TestBookDetailView(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='test_category')
        
        self.author = Author.objects.create(username='test', email='test@gmail.com', age=20)
        
        self.publisher = Publisher.objects.create(username='test', email='test@gmail.com', age=20)
        
        self.book = Book.objects.create(
            author=self.author, publisher=self.publisher, category=self.category,
            title='test', description='test description', isbn='123', slug='test',
            avatar='c://test/vm.jpg', total_copies=10, available_copies=10, published_date='2025-06-11'
        )

        self.url = reverse('books:book_detail',args=[self.book.slug])

    def test_get_book_detail_validate_data(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response,'books/book_detail.html')
        self.assertEqual(response.status_code,200)

        self.assertEqual(response.context['book'],self.book)
        self.assertIn('book',response.context)

class TestBookFilterByAuthorView(TestCase):
    def setUp(self):
        self.url = reverse('books:book_filter_by_author')

        self.author = Author.objects.create(username='test', email='test@gmail.com', age=20)

    def test_get_book_filter_by_author_validate_data(self):
        response = self.client.get(self.url,{'author':self.author.username})

        self.assertTemplateUsed(response,'books/book_list.html')
        self.assertEqual(response.status_code,200)

        self.assertEqual(len(response.context['books']),0)
        self.assertIn('books',response.context)

class TestBookFilterByPublisherView(TestCase):
    def setUp(self):
        self.url = reverse('books:book_filter_by_publisher')
    
        self.publisher = Publisher.objects.create(username='test', email='test@gmail.com', age=20)

    def test_get_book_filter_by_publisher(self):
        response = self.client.get(self.url,{'publisher':self.publisher.username})

        self.assertTemplateUsed(response,'books/book_list.html')
        self.assertEqual(response.status_code,200)

        self.assertEqual(len(response.context['books']),0)
        self.assertIn('books',response.context)

class TestBookFilterByCategoryView(TestCase):
    def setUp(self):
        self.url = reverse('books:book_filter_by_category')

        self.category = Category.objects.create(name='test_category')
    
    def test_get_book_filter_by_category(self):
        response = self.client.get(self.url,{'category':self.category.name})

        self.assertTemplateUsed(response,'books/book_list.html')
        self.assertEqual(response.status_code,200)

        self.assertEqual(len(response.context['books']),0)
        self.assertIn('books',response.context)

class TestBookSearchView(TestCase):
    def setUp(self):
        self.url = reverse('books:book_search')
    
    def test_get_book_search_view(self):
        response = self.client.get(self.url,{'q':'test'})

        self.assertTemplateUsed(response,'books/book_list.html')
        self.assertEqual(response.status_code,200)

        self.assertIn('books',response.context)
        self.assertEqual(len(response.context['books']),0)

        self.assertIn('categories',response.context)
        self.assertEqual(len(response.context['categories']),0)

        self.assertIn('authors',response.context)
        self.assertEqual(len(response.context['authors']),0)

        self.assertIn('publishers',response.context)
        self.assertEqual(len(response.context['publishers']),0)

class TestBorrowTransactionListView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test', email='test@gmail.com', avatar='', passport='', 
            address='test', city='test', country='AF', birth_date='2020-01-02', email_verified=True,
            password='Test12345%'
        )

        self.url = reverse('books:borrow_transaction_list')
    
    def test_get_borrow_transaction_list(self):
        self.client.login(username='test', password='Test12345%')
        response = self.client.get(self.url)

        self.assertTemplateUsed(response,'books/borrow_transaction_list.html')
        self.assertEqual(response.status_code,200)

        self.assertEqual(len(response.context['borrows']),0)
        self.assertIn('borrows',response.context)

class TestBorrowTransactionCreateView(TestCase):
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
            avatar='c://test/cm.jpg', total_copies=10, available_copies=10, published_date='2025-06-11'
        )

        self.book_copy = BookCopy.objects.create(
            book=self.book, copy_number=2, location='test'
        )

        self.url = reverse('books:borrow_transaction_create',args=[self.book.slug])
    
    def test_post_borrow_transaction_create(self):
        self.client.login(username='test', password='Test12345%')
        response = self.client.post(self.url,data={'q':2})
        
        self.assertRedirects(response,reverse('books:borrow_transaction_list'))
        self.assertEqual(response.status_code,302)

class TestReservedListView(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(
            username='test', email='test@gmail.com', avatar='', passport='', 
            address='test', city='test', country='AF', birth_date='2020-01-02', email_verified=True,
            password='Test12345%'
        )

        self.client.login(username='test', password='Test12345%')

        self.url = reverse('books:reserved_list')

    def test_get_reserved_list(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response,'books/reserved_list.html')
        self.assertEqual(response.status_code,200)

        self.assertEqual(len(response.context['reserve_books']),0)
        self.assertIn('reserve_books',response.context)
    
class TestReservationCreateView(TestCase):
    def setUp(self):
        self.client = Client()

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
            avatar='c://test/cm.jpg', total_copies=10, available_copies=10, published_date='2025-06-11'
        )

        self.book_copy = BookCopy.objects.create(
            book=self.book, copy_number=2, location='test'
        )

        self.client.login(username='test', password='Test12345%')

        self.url = reverse('books:reserved_create',args=[self.book.slug])

    def test_reservation_create(self):
        response = self.client.post(self.url,data={'q':self.book_copy.copy_number})

        self.assertRedirects(response,reverse('books:reserved_list'))
        self.assertEqual(response.status_code,302)

class TestReturnBorrowView(TestCase):
    def setUp(self):
        self.client = Client()

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
            avatar='c://test/cm.jpg', total_copies=10, available_copies=10, published_date='2025-06-11'
        )

        self.book_copy = BookCopy.objects.create(
            book=self.book, copy_number=2, location='test'
        )

        self.borrow_transaction = BorrowTransaction.objects.create(
            user=self.user, book_copy=self.book_copy, due_date='2025-06-11'
        )

        self.client.login(username='test', password='Test12345%')

        self.url = reverse('books:return_borrow',args=[self.borrow_transaction.id])
    
    def test_post_return_borrow(self):
        response = self.client.post(self.url)

        self.assertRedirects(response,reverse('books:borrow_transaction_list'))
        self.assertEqual(response.status_code,302)
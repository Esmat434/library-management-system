from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from books.models import(
    Author,Publisher,Category,Book,BookCopy
)

from dashboard.forms.book_copy_forms import (
    BookCopyCreationForm,BookCopyUpdateForm
)

User = get_user_model()

class TestBookCopyListView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test', email='test@gmail.com', avatar='', passport='', 
            address='test', city='test', country='AF',role='librarian', birth_date='2020-01-02', 
            email_verified=True,password='Test12345%'
        )
    
        self.client.login(username='test', password='Test12345%')

        self.url = reverse('dashboard:book_copy_list')

    def test_post_book_copy_list_view(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response,'dashboard/book_copy_list.html')
        self.assertEqual(response.status_code,200)

        self.assertIn('book_copy',response.context)
        self.assertEqual(len(response.context['book_copy']),0)
    
class TestBookCopyDetailView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test', email='test@gmail.com', avatar='', passport='', 
            address='test', city='test', country='AF',role='librarian', birth_date='2020-01-02', 
            email_verified=True,password='Test12345%'
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
    
        self.client.login(username='test', password='Test12345%')

        self.url = reverse('dashboard:book_copy_detail',args=[self.book_copy.id])

    def test_get_book_detail_view(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response,'dashboard/book_copy_detail.html')
        self.assertEqual(response.status_code,200)

        self.assertIn('book_copy',response.context)
        self.assertIsNotNone(response.context['book_copy'])

class TestBookCopyCreateView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test', email='test@gmail.com', avatar='', passport='', 
            address='test', city='test', country='AF',role='librarian', birth_date='2020-01-02', 
            email_verified=True,password='Test12345%'
        )

        self.category = Category.objects.create(name='test_category')
        
        self.author = Author.objects.create(username='test', email='test@gmail.com', age=20)
        
        self.publisher = Publisher.objects.create(username='test', email='test@gmail.com', age=20)
        
        self.book = Book.objects.create(
            author=self.author, publisher=self.publisher, category=self.category,
            title='test', description='test description', isbn='123', slug='test',
            avatar='', total_copies=10, available_copies=10, published_date='2025-06-11'
        )

        self.data = {
            'book':self.book.id,'copy_number':3,'status':'available','location':'test'
        }

        self.client.login(username='test', password='Test12345%')

        self.url = reverse('dashboard:book_copy_create')

    def test_get_book_copy_create_view(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response,'dashboard/book_copy_create.html')
        self.assertEqual(response.status_code,200)

        self.assertIn('form',response.context)
        self.assertIsInstance(response.context['form'],BookCopyCreationForm)
    
    def test_post_book_copy_create_view(self):
        response = self.client.post(self.url,data=self.data)

        self.assertRedirects(response,reverse('dashboard:book_copy_list'))
        self.assertEqual(response.status_code,302)

class TestBookCopyUpdateView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test', email='test@gmail.com', avatar='', passport='', 
            address='test', city='test', country='AF',role='librarian', birth_date='2020-01-02', 
            email_verified=True,password='Test12345%'
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
        
        self.data = {
            'book':self.book.id,'copy_number':5,'status':'borrowed','location':'change'
        }

        self.client.login(username='test', password='Test12345%')

        self.url = reverse('dashboard:book_copy_update',args=[self.book_copy.id])

    def test_get_book_copy_update_view(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response,'dashboard/book_copy_update.html')
        self.assertEqual(response.status_code,200)

        self.assertIn('form',response.context)
        self.assertIsInstance(response.context['form'],BookCopyUpdateForm)
    
    def test_post_book_copy_update_view(self):
        response = self.client.post(self.url,data=self.data)

        self.assertRedirects(response,reverse('dashboard:book_copy_detail',args=[self.book_copy.id]))
        self.assertEqual(response.status_code,302)

class TestBookCopyDeleteView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test', email='test@gmail.com', avatar='', passport='', 
            address='test', city='test', country='AF',role='librarian', birth_date='2020-01-02', 
            email_verified=True,password='Test12345%'
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
        
        self.data = {
            'book':self.book.id,'copy_number':5,'status':'borrowed','location':'change'
        }

        self.client.login(username='test', password='Test12345%')

        self.url = reverse('dashboard:book_copy_delete',args=[self.book_copy.id])

    def test_book_copy_delete_view(self):
        response = self.client.post(self.url)

        self.assertRedirects(response,reverse('dashboard:book_copy_list'))
        self.assertEqual(response.status_code,302)
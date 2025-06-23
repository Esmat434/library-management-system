from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from books.models import (
    Author,Publisher,Category,Book,BookCopy
)

from dashboard.forms.book_forms import (
    BookCreationForm,BookUpdateForm
)

User = get_user_model()

IMAGE_FILE_CONTENT = b'GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'

class TestBookListView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test', email='test@gmail.com', avatar='c://file/test.jpg', passport='c://file/test.jpg', 
            address='test', city='test', country='AF',role='librarian', birth_date='2020-01-02', email_verified=True,
            password='Test12345%'
        )

        self.client.login(username='test', password='Test12345%')

        self.url = reverse('dashboard:book_list')
    
    def test_get_book_list_book(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response,'dashboard/book_list.html')
        self.assertEqual(response.status_code,200)

        self.assertIn('books',response.context)
        self.assertEqual(len(response.context['books']),0)

class TestBookDetailView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test', email='test@gmail.com', avatar='c://file/test.jpg', passport='c://file/test.jpg', 
            address='test', city='test', country='AF',role='librarian', birth_date='2020-01-02', email_verified=True,
            password='Test12345%'
        )

        self.category = Category.objects.create(name='test_category')
        
        self.author = Author.objects.create(username='test', email='test@gmail.com', age=20)
        
        self.publisher = Publisher.objects.create(username='test', email='test@gmail.com', age=20)
        
        self.book = Book.objects.create(
            author=self.author, publisher=self.publisher, category=self.category,
            title='test', description='test description', isbn='123', slug='test',
            avatar='c://file/test.jpg', total_copies=10, available_copies=10, published_date='2025-06-11'
        )

        self.client.login(username='test', password='Test12345%')

        self.url = reverse('dashboard:book_detail',args=[self.book.slug])
    
    def test_get_book_detail_view(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response,'dashboard/book_detail.html')
        self.assertEqual(response.status_code,200)

        self.assertIn('book',response.context)
        self.assertIsNotNone(response.context['book'])

class TestBookCreateView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test', email='test@gmail.com', avatar='c://file/test.jpg', passport='c://file/test.jpg', 
            address='test', city='test', country='AF',role='librarian', birth_date='2020-01-02', email_verified=True,
            password='Test12345%'
        )

        self.category = Category.objects.create(name='test_category')
        
        self.author = Author.objects.create(username='test', email='test@gmail.com', age=20)
        
        self.publisher = Publisher.objects.create(username='test', email='test@gmail.com', age=20)
        
        self.avatar = SimpleUploadedFile(
            name='test_avatar.gif',
            content=IMAGE_FILE_CONTENT,
            content_type='image/gif'
        )

        self.data = {
            'author':self.author.id,'publisher':self.publisher.id,'category':self.category.id,
            'title':'test title','description':'test description','isbn':'123', 'slug':'test',
            'total_copies':10, 'available_copies':10, 'published_date':'2025-06-11'
        }

        self.file_data = {
            'avatar':self.avatar
        }

        self.client.login(username='test', password='Test12345%')

        self.url = reverse('dashboard:book_create')
    
    def test_get_book_create_view(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response,'dashboard/book_create.html')
        self.assertEqual(response.status_code,200)

        self.assertIn('form',response.context)
        self.assertIsInstance(response.context['form'],BookCreationForm)

    def test_post_book_create_view(self):
        data = {**self.data,**self.file_data}
        response = self.client.post(self.url,data=data,format='multipart')
        
        self.assertRedirects(response,reverse('dashboard:book_list'))
        self.assertEqual(response.status_code,302)

class TestBookUpdateView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test', email='test@gmail.com', avatar='c://file/test.jpg', passport='c://file/test.jpg', 
            address='test', city='test', country='AF',role='librarian', birth_date='2020-01-02', email_verified=True,
            password='Test12345%'
        )

        self.category = Category.objects.create(name='test_category')
        
        self.author = Author.objects.create(username='test', email='test@gmail.com', age=20)
        
        self.publisher = Publisher.objects.create(username='test', email='test@gmail.com', age=20)
        
        self.book = Book.objects.create(
            author=self.author, publisher=self.publisher, category=self.category,
            title='test', description='test description', isbn='123', slug='test',
            avatar='c://file/test.jpg', total_copies=10, available_copies=10, published_date='2025-06-11'
        )

        self.avatar = SimpleUploadedFile(
            name='test_avatar.gif',
            content=IMAGE_FILE_CONTENT,
            content_type='image/gif'
        )

        self.data = {
            'author':self.author.id,'publisher':self.publisher.id,'category':self.category.id,
            'title':'change title','description':'change description','isbn':'564', 'slug':'change',
            'total_copies':30, 'available_copies':20, 'published_date':'2025-06-11'
        }

        self.file_data = {
            'avatar':self.avatar
        }

        self.client.login(username='test', password='Test12345%')

        self.url = reverse('dashboard:book_update',args=[self.book.slug])

    def test_get_book_update_view(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response,'dashboard/book_update.html') 
        self.assertEqual(response.status_code,200)

        self.assertIn('form',response.context)
        self.assertIsInstance(response.context['form'],BookUpdateForm)

    def test_post_book_update_view(self):
        data = {**self.data,**self.file_data}
        response = self.client.post(self.url,data=data,format='multipart')   
        
        updated_book = Book.objects.get(id=self.book.id)
        self.assertRedirects(response,reverse('dashboard:book_detail',args=[updated_book.slug]))
        self.assertEqual(response.status_code,302)

class TestBookDeleteView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test', email='test@gmail.com', avatar='c://file/test.jpg', passport='c://file/test.jpg', 
            address='test', city='test', country='AF',role='librarian', birth_date='2020-01-02', email_verified=True,
            password='Test12345%'
        )

        self.category = Category.objects.create(name='test_category')
        
        self.author = Author.objects.create(username='test', email='test@gmail.com', age=20)
        
        self.publisher = Publisher.objects.create(username='test', email='test@gmail.com', age=20)
        
        self.book = Book.objects.create(
            author=self.author, publisher=self.publisher, category=self.category,
            title='test', description='test description', isbn='123', slug='test',
            avatar='c://file/test.jpg', total_copies=10, available_copies=10, published_date='2025-06-11'
        )

        self.client.login(username='test', password='Test12345%')

        self.url = reverse('dashboard:book_delete',args=[self.book.slug])

    def test_post_book_delete_view(self):
        response = self.client.post(self.url)

        self.assertRedirects(response,reverse('dashboard:book_list'))
        self.assertEqual(response.status_code,302)
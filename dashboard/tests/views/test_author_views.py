from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from books.models import (
    Author
)

from dashboard.forms.author_forms import (
    AuthorCreationForm,AuthorUpdateForm
)

User = get_user_model()

class TestAuthorListView(TestCase):
    def setUp(self):
        self.url = reverse('dashboard:author_list')
        self.user = User.objects.create_user(
            username='test', email='test@gmail.com', avatar='c://file/test.jpg', passport='c://file/test.jpg', 
            address='test', city='test', country='AF',role='admin', birth_date='2020-01-02', email_verified=True,
            password='Test12345%'
        )

        self.client.login(username='test', password='Test12345%')
    
    def test_get_author_list_view(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response,'dashboard/author_list.html')
        self.assertEqual(response.status_code,200)

        self.assertEqual(len(response.context['authors']),0)
        self.assertIn('authors',response.context)

class TestAuthorDetailView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test', email='test@gmail.com', avatar='c://file/test.jpg', passport='c://file/test.jpg', 
            address='test', city='test', country='AF',role='admin', birth_date='2020-01-02', email_verified=True,
            password='Test12345%'
        )

        self.author = Author.objects.create(username='test', email='test@gmail.com', age=20)
        
        self.url = reverse('dashboard:author_detail',args=[self.author.id])

        self.client.login(username='test', password='Test12345%')
    
    def test_get_author_detail_view(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response,'dashboard/author_detail.html')
        self.assertEqual(response.status_code,200)

        self.assertIn('author',response.context)
        self.assertIsNotNone(response.context['author'])
        
class TestAuthorCreateView(TestCase):
    def setUp(self):
        self.url = reverse('dashboard:author_create')
        
        self.user = User.objects.create_user(
            username='test', email='test@gmail.com', avatar='c://file/test.jpg', passport='c://file/test.jpg', 
            address='test', city='test', country='AF',role='admin', birth_date='2020-01-02', email_verified=True,
            password='Test12345%'
        )

        self.data = {
            'username':'test','email':'test@gmail.com','age':15
        }

        self.client.login(username='test', password='Test12345%')
    
    def test_get_author_create_view(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response,'dashboard/author_create.html')
        self.assertEqual(response.status_code,200)

        self.assertIn('form',response.context)
        self.assertIsInstance(response.context['form'],AuthorCreationForm)
    
    def test_post_author_create_view(self):
        response = self.client.post(self.url,data=self.data)

        self.assertRedirects(response,reverse('dashboard:author_list'))
        self.assertEqual(response.status_code,302)

class TestAuthorUpdateView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test', email='test@gmail.com', avatar='c://file/test.jpg', passport='c://file/test.jpg', 
            address='test', city='test', country='AF',role='admin', birth_date='2020-01-02', email_verified=True,
            password='Test12345%'
        )

        self.author = Author.objects.create(username='test', email='test@gmail.com', age=20)

        self.data = {
            'username':'change','email':'test@gmail.com','age':30
        }

        self.client.login(username='test', password='Test12345%')

        self.url = reverse('dashboard:author_update',args=[self.author.id])

    def test_get_author_update_view(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response,'dashboard/author_update.html')
        self.assertEqual(response.status_code,200)

        self.assertIn('form',response.context)
        self.assertIsInstance(response.context['form'],AuthorUpdateForm)
    
    def test_post_author_update_view(self):
        response = self.client.post(self.url,data=self.data)

        self.assertRedirects(response,reverse('dashboard:author_detail',args=[self.author.id]))
        self.assertEqual(response.status_code,302)

class TestAuthorDeleteView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test', email='test@gmail.com', avatar='c://file/test.jpg', passport='c://file/test.jpg', 
            address='test', city='test', country='AF',role='admin', birth_date='2020-01-02', email_verified=True,
            password='Test12345%'
        )

        self.author = Author.objects.create(username='test', email='test@gmail.com', age=20)

        self.client.login(username='test', password='Test12345%')

        self.url = reverse('dashboard:author_delete',args=[self.author.id])
    
    def test_post_author_delete_view(self):
        response = self.client.post(self.url)

        self.assertRedirects(response,reverse('dashboard:author_list'))
        self.assertEqual(response.status_code,302)

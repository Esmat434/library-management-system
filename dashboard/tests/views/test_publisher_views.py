from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from books.models import (
    Publisher
)

from dashboard.forms.publisher_forms import (
    PublisherCreationForm,PublisherUpdateForm
)

User = get_user_model()

class TestPublisherListView(TestCase):
    def setUp(self):
        self.url = reverse('dashboard:publisher_list')
        self.user = User.objects.create_user(
            username='test', email='test@gmail.com', avatar='', passport='', 
            address='test', city='test', country='AF',role='admin', birth_date='2020-01-02', email_verified=True,
            password='Test12345%'
        )

        self.client.login(username='test', password='Test12345%')
    
    def test_get_author_list_view(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response,'dashboard/publisher_list.html')
        self.assertEqual(response.status_code,200)

        self.assertEqual(len(response.context['publishers']),0)
        self.assertIn('publishers',response.context)

class TestPublisherDetailView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test', email='test@gmail.com', avatar='', passport='', 
            address='test', city='test', country='AF',role='admin', birth_date='2020-01-02', email_verified=True,
            password='Test12345%'
        )

        self.publisher = Publisher.objects.create(username='test', email='test@gmail.com', age=20)
        
        self.url = reverse('dashboard:publisher_detail',args=[self.publisher.id])

        self.client.login(username='test', password='Test12345%')
    
    def test_get_publisher_detail_view(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response,'dashboard/publisher_detail.html')
        self.assertEqual(response.status_code,200)

        self.assertIn('publisher',response.context)
        self.assertIsNotNone(response.context['publisher'])
        
class TestPublisherCreateView(TestCase):
    def setUp(self):
        self.url = reverse('dashboard:publisher_create')
        
        self.user = User.objects.create_user(
            username='test', email='test@gmail.com', avatar='', passport='', 
            address='test', city='test', country='AF',role='admin', birth_date='2020-01-02', email_verified=True,
            password='Test12345%'
        )

        self.data = {
            'username':'test','email':'test@gmail.com','age':15
        }

        self.client.login(username='test', password='Test12345%')
    
    def test_get_publsiher_create_view(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response,'dashboard/publisher_create.html')
        self.assertEqual(response.status_code,200)

        self.assertIn('form',response.context)
        self.assertIsInstance(response.context['form'],PublisherCreationForm)
    
    def test_post_publisher_create_view(self):
        response = self.client.post(self.url,data=self.data)

        self.assertRedirects(response,reverse('dashboard:publisher_list'))
        self.assertEqual(response.status_code,302)

class TestPublisherUpdateView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test', email='test@gmail.com', avatar='', passport='', 
            address='test', city='test', country='AF',role='admin', birth_date='2020-01-02', email_verified=True,
            password='Test12345%'
        )

        self.publisher = Publisher.objects.create(username='test', email='test@gmail.com', age=20)

        self.data = {
            'username':'change','email':'test@gmail.com','age':30
        }

        self.client.login(username='test', password='Test12345%')

        self.url = reverse('dashboard:publisher_update',args=[self.publisher.id])

    def test_get_publisher_update_view(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response,'dashboard/publisher_update.html')
        self.assertEqual(response.status_code,200)

        self.assertIn('form',response.context)
        self.assertIsInstance(response.context['form'],PublisherUpdateForm)
    
    def test_post_publisher_update_view(self):
        response = self.client.post(self.url,data=self.data)

        self.assertRedirects(response,reverse('dashboard:publisher_detail',args=[self.publisher.id]))
        self.assertEqual(response.status_code,302)

class TestPublisherDeleteView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test', email='test@gmail.com', avatar='', passport='', 
            address='test', city='test', country='AF',role='admin', birth_date='2020-01-02', email_verified=True,
            password='Test12345%'
        )

        self.publisher = Publisher.objects.create(username='test', email='test@gmail.com', age=20)

        self.client.login(username='test', password='Test12345%')

        self.url = reverse('dashboard:publisher_delete',args=[self.publisher.id])
    
    def test_post_author_delete_view(self):
        response = self.client.post(self.url)

        self.assertRedirects(response,reverse('dashboard:publisher_list'))
        self.assertEqual(response.status_code,302)
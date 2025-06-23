from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from books.models import (
    Category
)

from dashboard.forms.category_forms import (
    CategoryCreationForm,CategoryUpdateForm
)

User = get_user_model()

class TestCategoryListView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test', email='test@gmail.com', avatar='c://file/test.jpg', passport='c://file/test.jpg', 
            address='test', city='test', country='AF',role='librarian', birth_date='2020-01-02', email_verified=True,
            password='Test12345%'
        )

        self.client.login(username='test', password='Test12345%')

        self.url = reverse('dashboard:category_list')
    
    def test_get_category_list_view(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response,'dashboard/category_list.html')
        self.assertEqual(response.status_code,200)

        self.assertIn('categories',response.context)
        self.assertEqual(len(response.context['categories']),0)
    
class TestCategoryDetailView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test', email='test@gmail.com', avatar='c://file/test.jpg', passport='c://file/test.jpg', 
            address='test', city='test', country='AF',role='librarian', birth_date='2020-01-02', email_verified=True,
            password='Test12345%'
        )

        self.category = Category.objects.create(name='test name',description='test description')

        self.client.login(username='test', password='Test12345%')

        self.url = reverse('dashboard:category_detail',args=[self.category.id])
    
    def test_get_category_detail_view(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response,'dashboard/category_detail.html')
        self.assertEqual(response.status_code,200)

        self.assertIn('category',response.context)
        self.assertIsNotNone(response.context['category'])
    
class TestCategoryCreateView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test', email='test@gmail.com', avatar='c://file/test.jpg', passport='c://file/test.jpg', 
            address='test', city='test', country='AF',role='librarian', birth_date='2020-01-02', email_verified=True,
            password='Test12345%'
        )

        self.data = {
            'name':'test name','description':'test description'
        }

        self.client.login(username='test', password='Test12345%')

        self.url = reverse('dashboard:category_create')
    
    def test_get_category_create_view(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response,'dashboard/category_create.html')
        self.assertEqual(response.status_code,200)

        self.assertIn('form',response.context)
        self.assertIsInstance(response.context['form'],CategoryCreationForm)
    
    def test_post_category_create_view(self):
        response = self.client.post(self.url,data=self.data)

        self.assertRedirects(response,reverse('dashboard:category_list'))
        self.assertEqual(response.status_code,302)

class TestCategoryUpdateView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test', email='test@gmail.com', avatar='c://file/test.jpg', passport='c://file/test.jpg', 
            address='test', city='test', country='AF',role='librarian', birth_date='2020-01-02', email_verified=True,
            password='Test12345%'
        )

        self.category = Category.objects.create(name='test name',description='test description')

        self.data = {
            'name':'change name','description':'change description'
        }

        self.client.login(username='test', password='Test12345%')

        self.url = reverse('dashboard:category_update',args=[self.category.id])
    
    def test_get_category_update_view(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response,'dashboard/category_update.html')
        self.assertEqual(response.status_code,200)

        self.assertIn('form',response.context)
        self.assertIsInstance(response.context['form'],CategoryUpdateForm)
    
    def test_post_category_update_view(self):
        response = self.client.post(self.url,data=self.data)

        self.assertRedirects(response,reverse('dashboard:category_detail',args=[self.category.id]))
        self.assertEqual(response.status_code,302)

class TestCategoryDeleteView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test', email='test@gmail.com', avatar='c://file/test.jpg', passport='c://file/test.jpg', 
            address='test', city='test', country='AF',role='librarian', birth_date='2020-01-02', email_verified=True,
            password='Test12345%'
        )

        self.category = Category.objects.create(name='test name',description='test description')

        self.client.login(username='test', password='Test12345%')

        self.url = reverse('dashboard:category_delete',args=[self.category.id])
    
    def test_post_category_delete_view(self):
        response = self.client.post(self.url)

        self.assertRedirects(response,reverse('dashboard:category_list'))
        self.assertEqual(response.status_code,302)
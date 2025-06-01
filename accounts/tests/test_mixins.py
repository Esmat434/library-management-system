from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class TestLoginRequiredMixin(TestCase):
    def setUp(self):
        self.url = reverse('accounts:profile')

        self.user = User.objects.create_user(
            username='test', email='test@gmail.com', avatar='', passport='', 
            address='test', city='test', country='AF', birth_date='2020-01-02', email_verified=True,
            password='Test12345%'
        )
    
    def test_redirect_if_not_login(self):
        response = self.client.get(self.url)

        self.assertRedirects(response,reverse('accounts:login'))
        self.assertEqual(response.status_code,302)

    def test_render_if_login(self):
        self.client.login(username='test', password='Test12345%')
        response = self.client.get(self.url)

        self.assertTemplateUsed(response,'accounts/profile.html')
        self.assertEqual(response.status_code,200)
        
class TestLogoutRequiredMixin(TestCase):
    def setUp(self):
        self.url = reverse('accounts:register')

        self.user = User.objects.create_user(
            username='test', email='test@gmail.com', avatar='', passport='', 
            address='test', city='test', country='AF', birth_date='2020-01-02', email_verified=True,
            password='Test12345%'
        )
    
    def test_redirect_if_login(self):
        self.client.login(username='test', password='Test12345%')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code,302)
    
    def test_render_if_not_login(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response,'accounts/register.html')
        self.assertEqual(response.status_code,200)
        
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class TestLoginRequired(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test', email='test@gmail.com', avatar='', passport='', 
            address='test', city='test', country='AF',role='admin', birth_date='2020-01-02', email_verified=True,
            password='Test12345%'
        )

        self.url = reverse('dashboard:author_list')

    def test_redirect_if_not_login(self):
        response = self.client.get(self.url)

        self.assertRedirects(response,reverse('accounts:login'))
        self.assertEqual(response.status_code,302)
    
    def test_render_if_login_and_user_is_admin_or_is_librarian(self):
        self.client.login(username='test', password='Test12345%')
        response = self.client.get(self.url)

        self.assertTemplateUsed(response,'dashboard/author_list.html')
        self.assertEqual(response.status_code,200)
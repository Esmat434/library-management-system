from django.test import TestCase
from django.urls import reverse

class TestAboutUsView(TestCase):
    def setUp(self):
        self.url = reverse('core:about_us')
    
    def test_get_about_us(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response,'core/about_us.html')
        self.assertEqual(response.status_code,200)
    
class TestContactUsView(TestCase):
    def setUp(self):
        self.url = reverse('core:contact_us')

        self.data = {
            'username':'test','email':'test@gmail.com','phone_number':'0771220009',
            'title':'test title','message':'test message'
        }

    def test_get_contact_us(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response,'core/contact_us.html')
        self.assertEqual(response.status_code,200)
    
    def test_post_contact_us(self):
        response = self.client.post(self.url,data=self.data)

        self.assertRedirects(response,reverse('books:home'))
        self.assertEqual(response.status_code,302)
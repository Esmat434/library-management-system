from django.test import SimpleTestCase
from django.urls import reverse

class TestUrls(SimpleTestCase):
    def test_about_us_url(self):
        url_name = 'core:about_us'
        url_path = reverse(url_name)

        self.assertEqual(url_path,'/about/')

    def test_contact_us_url(self):
        url_name = 'core:contact_us'
        url_path = reverse(url_name)

        self.assertEqual(url_path,'/contact/')
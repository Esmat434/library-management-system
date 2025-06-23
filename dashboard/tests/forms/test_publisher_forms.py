from django.test import TestCase

from books.models import (
    Publisher
)

from dashboard.forms.publisher_forms import (
    PublisherCreationForm,PublisherUpdateForm
)

class TestPublisherCreationForm(TestCase):
    def setUp(self):
        self.data = {
            'username':'test','email':'test@gmail.com','first_name':'test','last_name':'test',
            'phone_number':'0771450009','age':20,'address':'test address'
        }
    
    def test_publisher_create_form_validate_data(self):
        form = PublisherCreationForm(data=self.data)

        self.assertTrue(form.is_valid())

class TestAuthorUpdateForm(TestCase):
    def setUp(self):
        self.data = {
            'username':'test change','email':'testchange@gmail.com','first_name':'test change','last_name':'test',
            'phone_number':'0771450009','age':20,'address':'test address'
        }

        self.publisher = Publisher.objects.create(username='test', email='test@gmail.com', age=20)
    
    def test_publisher_update_form_validate_data(self):
        form = PublisherUpdateForm(data=self.data,instance=self.publisher)

        self.assertTrue(form.is_valid())
from django.test import TestCase

from books.models import (
    Author
)

from dashboard.forms.author_forms import (
    AuthorCreationForm,AuthorUpdateForm
)

class TestAuthorCreationForm(TestCase):
    def setUp(self):
        self.data = {
            'username':'test','email':'test@gmail.com','first_name':'test','last_name':'test',
            'phone_number':'0771450009','age':20,'address':'test address'
        }
    
    def test_author_create_form_validate_data(self):
        form = AuthorCreationForm(data=self.data)

        self.assertTrue(form.is_valid())

class TestAuthorUpdateForm(TestCase):
    def setUp(self):
        self.data = {
            'username':'test change','email':'testchange@gmail.com','first_name':'test change','last_name':'test',
            'phone_number':'0771450009','age':20,'address':'test address'
        }

        self.author = Author.objects.create(username='test', email='test@gmail.com', age=20)
    
    def test_author_update_form_validate_data(self):
        form = AuthorUpdateForm(data=self.data,instance=self.author)

        self.assertTrue(form.is_valid())
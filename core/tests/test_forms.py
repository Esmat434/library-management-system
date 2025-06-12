from django.test import TestCase

from core.forms import (
    ContactCreationForm
)

class TestContactCreationForm(TestCase):
    def setUp(self):
        self.data = {
            'username':'test','email':'test@gmail.com','phone_number':'0771240006',
            'title':'test title','message':'test message'
        }
    
    def test_contact_creation_form(self):
        form = ContactCreationForm(self.data)
        
        self.assertTrue(form.is_valid())
        
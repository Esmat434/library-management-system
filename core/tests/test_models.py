from django.test import TestCase

from core.models import (
    Contact
)

class TestContactModel(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(
            username='test',email='test@gmail.com',phone_number='77123002',title='test title',
            message='test message'
        )
    
    def test_contact_validate_data(self):
        self.assertEqual(self.contact.username,'test')
        self.assertEqual(self.contact.email,'test@gmail.com')
        self.assertEqual(self.contact.title,'test title')
        
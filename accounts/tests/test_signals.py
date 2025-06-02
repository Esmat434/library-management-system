from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.models import AccountVerificationToken

User = get_user_model()

class TestAccountVerifiedTokenSignal(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test', email='test@gmail.com', avatar='', passport='', 
            address='test', city='test', country='AF', birth_date='2020-01-02', email_verified=True,
            password='Test12345%'
        )

    def test_account_verified_token_created_when_user_create(self):
        self.assertTrue(AccountVerificationToken.objects.filter(user=self.user).exists())
    
    def tearDown(self):
        token =  AccountVerificationToken.objects.filter(user = self.user)
        if token.exists():
            token.delete()
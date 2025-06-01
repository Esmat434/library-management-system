from django.test import TestCase

from accounts.models import (
    CustomUser,AccountVerificationToken,ChangePasswordToken,
    ForgotPasswordToken
)

class TestCustomUserModel(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='test', email='test@gmail.com', avatar='', passport='', 
            address='test', city='test', country='AF', birth_date='2020-01-02', email_verified=True,
            password='Test12345%'
        )
    
    def test_customuser_model_validate(self):
        self.assertEqual(self.user.username,'test')
        self.assertEqual(self.user.email,'test@gmail.com')

class TestAccountVerificationTokenModel(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='test', email='test@gmail.com', avatar='', passport='', 
            address='test', city='test', country='AF', birth_date='2020-01-02', email_verified=True,
            password='Test12345%'
        )
        
        self.token = AccountVerificationToken.objects.create(
            user = self.user
        )
    
    def test_account_verification_token_model_validate(self):
        token_instance = AccountVerificationToken.objects.get(user = self.user)

        self.assertEqual(token_instance.token,self.token.token)
        self.assertEqual(self.token.user,self.user)
    
    def test_is_expired_method_validate(self):
        self.assertFalse(self.token.is_expired())

class TestChangePasswordTokenModel(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='test', email='test@gmail.com', avatar='', passport='', 
            address='test', city='test', country='AF', birth_date='2020-01-02', email_verified=True,
            password='Test12345%'
        )

        self.token = ChangePasswordToken.objects.create(
            user = self.user
        )
    
    def test_change_password_token_model_validate(self):
        token_instance = ChangePasswordToken.objects.get(user=self.user)

        self.assertEqual(self.token.token,token_instance.token)
        self.assertEqual(self.token.user,self.user)
    
    def test_is_expired_method_validate(self):
        self.assertFalse(self.token.is_expired())

class TestForgotPasswordTokenModel(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='test', email='test@gmail.com', avatar='', passport='', 
            address='test', city='test', country='AF', birth_date='2020-01-02', email_verified=True,
            password='Test12345%'
        )

        self.token = ForgotPasswordToken.objects.create(
            user=self.user
        )
    
    def test_forgot_password_token_model_validate(self):
        token_instance = ForgotPasswordToken.objects.get(user=self.user)

        self.assertEqual(self.token.token,token_instance.token)
        self.assertEqual(self.token.user,self.user)
    
    def test_is_expired_method_validate(self):
        self.assertFalse(self.token.is_expired())
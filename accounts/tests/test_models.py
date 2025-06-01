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

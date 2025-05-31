from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from accounts.forms import (
    UserForm,UserUpdateForm,ChangePasswordForm,ForgotPasswordForm
)

from accounts.models import (
    CustomUser,AccountVerificationToken,ChangePasswordToken,ForgotPasswordToken
)

IMAGE_FILE_CONTENT = b'GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'

class TestRegisterView(TestCase):
    def setUp(self):
        self.url = reverse('accounts:register')

        self.avatar_file = SimpleUploadedFile(
            name='test_avatar.gif',
            content=IMAGE_FILE_CONTENT,
            content_type='image/gif'
        )

        self.passport_file = SimpleUploadedFile(
            name='test_passport.gif',
            content=IMAGE_FILE_CONTENT,
            content_type='image/gif'
        )

        self.form_data = {
            'username':'test','email':'test@gmail.com','first_name':'test','last_name':'testi',
            'phone_number':'+93771230009','address':'address','city':'city','country':'AF',
            'birth_date':'2000-01-02','password':'Test9999$','password1':'Test9999$'
        }
    
    def test_get_register_view_validate(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response,'accounts/register.html')
        self.assertEqual(response.status_code,200)

        self.assertIn('form',response.context)
        form = response.context['form']
        self.assertIsInstance(form,UserForm)
        self.assertFalse(form.is_bound)
    
    def test_post_register_view_validate(self):
        data = {
            **self.form_data,
            'avatar': self.avatar_file,
            'passport': self.passport_file
        }
        response = self.client.post(self.url, data=data, format='multipart')
        
        self.assertTemplateUsed(response,'accounts/account_verified_message.html')
        self.assertEqual(response.status_code,200)

class TestAcountVerifiedToken(TestCase):
    def setUp(self):
        self.avatar_file = SimpleUploadedFile(
            name='test_avatar.gif',
            content=IMAGE_FILE_CONTENT,
            content_type='image/gif'
        )

        self.passport_file = SimpleUploadedFile(
            name='test_passport.gif',
            content=IMAGE_FILE_CONTENT,
            content_type='image/gif'
        )

        self.user = CustomUser.objects.create_user(
            username='test', email='test@gmail.com', avatar=self.avatar_file, passport=self.passport_file, 
            address='test', city='test', country='AF', birth_date='2020-01-02'
        )

        self.token = AccountVerificationToken.objects.create(
            user = self.user
        )

        self.url = reverse('accounts:account_verified_token',args=[self.token.token])
    
    def test_get_account_verified_token_view_validate(self):
        response = self.client.get(self.url)
        self.assertRedirects(response,reverse('accounts:login'))
        self.assertEqual(response.status_code,302)

class TestResendAccountVerifiedTokenView(TestCase):
    def setUp(self):
        self.url = reverse('accounts:resend_account_token')
        
        self.avatar_file = SimpleUploadedFile(
            name='test_avatar.gif',
            content=IMAGE_FILE_CONTENT,
            content_type='image/gif'
        )

        self.passport_file = SimpleUploadedFile(
            name='test_passport.gif',
            content=IMAGE_FILE_CONTENT,
            content_type='image/gif'
        )
        
        self.user = CustomUser.objects.create_user(
            username='test', email='test@gmail.com', avatar=self.avatar_file, passport=self.passport_file, 
            address='test', city='test', country='AF', birth_date='2020-01-02'
        )
        
        self.data = {
            'email':'test@gmail.com'
        }

    def test_get_resend_account_verified_token_view_validate(self):
        response = self.client.get(self.url)
        
        self.assertTemplateUsed(response,'accounts/resend_account_verified_token.html')
        self.assertEqual(response.status_code,200)
    
    def test_post_resend_account_verified_token_view_validate(self):
        response = self.client.post(self.url, data=self.data)

        self.assertTemplateUsed(response,'accounts/account_verified_message.html')
        self.assertEqual(response.status_code,200)
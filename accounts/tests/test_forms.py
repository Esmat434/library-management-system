from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from accounts.forms import (
    UserForm,UserUpdateForm
)

User = get_user_model()

IMAGE_FILE_CONTENT = b'GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'

class TestUserForm(TestCase):
    
    def test_user_form_validate(self):
        avatar_file = SimpleUploadedFile(
            name='test_avatar.gif',
            content=IMAGE_FILE_CONTENT,
            content_type='image/gif'
        )
        passport_file = SimpleUploadedFile(
            name='test_passport.gif',
            content=IMAGE_FILE_CONTENT,
            content_type='image/gif'
        )

        form_data = {
            'username':'ahmad','email':'ahmadi@gmail.com','first_name':'ahmad','last_name':'ahmadi',
            'phone_number':'+93771230009','address':'address','city':'city',
            'country':'AF','birth_date':'2000-01-02','password':'Test12345%',
            'password1':'Test12345%'
        }
        file_data = {
            'avatar':avatar_file,
            'passport':passport_file
        }
        form = UserForm(form_data,file_data)
        
        self.assertEqual(form.is_valid(),True)

class TestUpdateUserForm(TestCase):
    def setUp(self):
        avatar_file = SimpleUploadedFile(
            name='test_avatar.gif',
            content=IMAGE_FILE_CONTENT,
            content_type='image/gif'
        )
        passport_file = SimpleUploadedFile(
            name='test_passport.gif',
            content=IMAGE_FILE_CONTENT,
            content_type='image/gif'
        )
        self.user = User.objects.create_user(
            username = 'test',email = 'test@gmail.com',avatar = avatar_file,passport = passport_file,
            address = 'address',city = 'city',country = 'AF',birth_date = '2000-03-01',
            password = 'Test12345%'
        )

        self.form_data = {
            'username':'test_ini','email':'test_ini@gmail.com','first_name':'testing','last_name':'testing',
            'phone_number':'+93771230009','address':'address','city':'city',
            'country':'AF','birth_date':'2005-01-02'
        }

    def test_update_user_form_validate(self):
        form = UserUpdateForm(self.form_data,instance=self.user)
        
        self.assertEqual(form.is_valid(),True)
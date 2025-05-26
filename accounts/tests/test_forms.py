from datetime import date
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from accounts.forms import (
    UserForm
)

from accounts.models import (
    CustomUser
)

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
            'phone_number':'+93771230009','address':'timany','city':'kabul',
            'country':'AF','birth_date':'2000-01-02','password':'Afghan111%',
            'password1':'Afghan111%'
        }
        file_data = {
            'avatar':avatar_file,
            'passport':passport_file
        }
        form = UserForm(form_data,file_data)
        
        self.assertEqual(form.is_valid(),True)
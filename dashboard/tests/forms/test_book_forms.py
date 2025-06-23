from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from books.models import (
    Author,Publisher,Category,Book
)

from dashboard.forms.book_forms import (
    BookCreationForm,BookUpdateForm
)

IMAGE_FILE_CONTENT = b'GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'

class TestBookCreationForm(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='test_category')
        
        self.author = Author.objects.create(username='test', email='test@gmail.com', age=20)
        
        self.publisher = Publisher.objects.create(username='test', email='test@gmail.com', age=20)
        
        self.avatar = SimpleUploadedFile(
            name='test_avatar.gif',
            content=IMAGE_FILE_CONTENT,
            content_type='image/gif'
        )

        self.data = {
            'author':self.author.id,'publisher':self.publisher.id,'category':self.category.id,
            'title':'test title','description':'test description','isbn':'123','slug':'test',
            'total_copies':0,'available_copies':0,'published_date':'2025-02-01'
        }
        self.file_data={
            'avatar':self.avatar
        }
    
    def test_book_creation_form_validate_data(self):
        form = BookCreationForm(data=self.data,files=self.file_data)

        self.assertTrue(form.is_valid())

class TestBookUpdateForm(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='test_category')
        
        self.author = Author.objects.create(username='test', email='test@gmail.com', age=20)
        
        self.publisher = Publisher.objects.create(username='test', email='test@gmail.com', age=20)
        
        self.avatar = SimpleUploadedFile(
            name='test_avatar.gif',
            content=IMAGE_FILE_CONTENT,
            content_type='image/gif'
        )

        self.data = {
            'author':self.author.id,'publisher':self.publisher.id,'category':self.category.id,
            'title':'change title','description':'change description','isbn':'39483','slug':'change',
            'total_copies':5,'available_copies':10,'published_date':'2025-02-01'
        }

        self.file_data = {
            'avatar':self.avatar
        }

        self.book = Book.objects.create(
            author=self.author, publisher=self.publisher, category=self.category,
            title='test title', description='test description', isbn='123', slug='test',
            avatar='', total_copies=0, available_copies=0, published_date='2025-06-11'
        )
    
    def test_book_update_form_validate_data(self):
        form = BookUpdateForm(data=self.data,files=self.file_data,instance=self.book)
        self.assertTrue(form.is_valid())
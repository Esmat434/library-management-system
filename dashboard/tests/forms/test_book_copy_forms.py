from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from books.models import (
    Author,Publisher,Category,Book,BookCopy
)

from dashboard.forms.book_copy_forms import (
    BookCopyCreationForm,BookCopyUpdateForm
)

class TestBookCopyCreationForm(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='test_category')
        
        self.author = Author.objects.create(username='test', email='test@gmail.com', age=20)
        
        self.publisher = Publisher.objects.create(username='test', email='test@gmail.com', age=20)
        
        self.book = Book.objects.create(
            author=self.author, publisher=self.publisher, category=self.category,
            title='test', description='test description', isbn='123', slug='test',
            avatar='', total_copies=10, available_copies=10, published_date='2025-06-11'
        )

        self.data = {
            'book':self.book.id,'copy_number':1,'status':'available','location':'test location'
        }
    
    def test_book_copy_creation_form(self):
        form = BookCopyCreationForm(data=self.data)

        self.assertTrue(form.is_valid())

class TestBookCopyUpdateForm(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='test_category')
        
        self.author = Author.objects.create(username='test', email='test@gmail.com', age=20)
        
        self.publisher = Publisher.objects.create(username='test', email='test@gmail.com', age=20)
        
        self.book = Book.objects.create(
            author=self.author, publisher=self.publisher, category=self.category,
            title='test', description='test description', isbn='123', slug='test',
            avatar='', total_copies=10, available_copies=10, published_date='2025-06-11'
        )

        self.book_copy = BookCopy.objects.create(
            book=self.book, copy_number=2, location='test'
        )

        self.data = {
            'book':self.book.id, 'copy_number':10,'status':'available','location':'change location'
        }
    
    def test_book_copy_update_form_validate_data(self):
        form = BookCopyUpdateForm(data=self.data,instance=self.book_copy)

        self.assertTrue(form.is_valid())
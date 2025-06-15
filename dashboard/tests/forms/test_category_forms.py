from django.test import TestCase 

from books.models import (
    Category
)

from dashboard.forms.category_forms import (
    CategoryCreationForm,CategoryUpdateForm
)

class TestCategoryCreationForm(TestCase):
    def setUp(self):
        self.data = {
            'name':'test name','description':'test description'
        }
    
    def test_category_creation_form_validate_data(self):
        form = CategoryCreationForm(data=self.data)

        self.assertTrue(form.is_valid())

class TestCategoryUpdateForm(TestCase):
    def setUp(self):
        self.data = {
            'name':'change title','description':'change title'
        }

        self.category = Category.objects.create(name='test title', description='test description')
    
    def test_category_update_form_validate_data(self):
        form = CategoryUpdateForm(data=self.data,instance=self.category)
        
        self.assertTrue(form.is_valid())
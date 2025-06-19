from django.test import SimpleTestCase
from django.urls import reverse

class TestUrls(SimpleTestCase):
    
    def test_book_list_url_is_reversed(self):
        url_name = 'books:home'
        url_path = reverse(url_name)
        self.assertEqual(url_path,'/')
        
    def test_book_detail_url_is_reversed(self):
        url_name = 'books:book_detail'
        url_path = reverse(url_name,args=['test'])
        self.assertEqual(url_path,'/books/test/')

    def test_book_filter_by_author_url_is_reversed(self):
        url_name = 'books:book_filter_by_author'
        url_path = reverse(url_name)
        self.assertEqual(url_path,'/books/filter/author/')
    
    def test_book_filter_by_category_url_is_reversed(self):
        url_name = 'books:book_filter_by_category'
        url_path = reverse(url_name)
        self.assertEqual(url_path,'/books/filter/category/')
    
    def test_book_filter_by_publisher_url_is_reversed(self):
        url_name = 'books:book_filter_by_publisher'
        url_path = reverse(url_name)
        self.assertEqual(url_path,'/books/filter/publisher/')

    def test_book_search_url_is_reversed(self):
        url_name = 'books:book_search'
        url_path = reverse(url_name)
        self.assertEqual(url_path,'/book/search/data/')
    
    def test_borrow_url_is_reversed(self):
        url_name = 'books:borrow_transaction_list'
        url_path = reverse(url_name)
        self.assertEqual(url_path,'/borrow/')
    
    def test_borrow_create_url_is_reversed(self):
        url_name = 'books:borrow_transaction_create'
        url_path = reverse(url_name,args=['test'])
        self.assertEqual(url_path,'/borrow/test/')
    
    def test_reserved_url_is_reversed(self):
        url_name = 'books:reserved_list'
        url_path = reverse(url_name)
        self.assertEqual(url_path,'/reserved/')
    
    def test_reserved_create_url_is_reversed(self):
        url_name = 'books:reserved_create'
        url_path = reverse(url_name,args=['test'])
        self.assertEqual(url_path,'/reserved/test/')
    
    def test_return_borrow_url_is_reversed(self):
        url_name = 'books:return_borrow'
        url_path = reverse(url_name,args=[1])
        self.assertEqual(url_path,'/return_borrow/1/')
from django.test import SimpleTestCase
from django.urls import reverse

class TestUrls(SimpleTestCase):
    def test_author_url(self):
        urlname = 'dashboard:author_list'
        url_path = reverse(urlname)

        self.assertEqual(url_path,'/dashboard/authors/')
    
    def test_author_detail_url(self):
        urlname = 'dashboard:author_detail'
        url_path = reverse(urlname,args=[1])

        self.assertEqual(url_path,'/dashboard/author/detail/1/')
    
    def test_author_create_url(self):
        urlname = 'dashboard:author_create'
        url_path = reverse(urlname)

        self.assertEqual(url_path,'/dashboard/author/create/')
    
    def test_author_update_url(self):
        urlname = 'dashboard:author_update'
        url_path = reverse(urlname,args=[1])

        self.assertEqual(url_path,'/dashboard/author/update/1/')
    
    def test_author_delete_url(self):
        urlname = 'dashboard:author_delete'
        url_path = reverse(urlname,args=[1])

        self.assertEqual(url_path,'/dashboard/author/delete/1/')
    
    def test_publisher_url(self):
        urlname = 'dashboard:publisher_list'
        url_path = reverse(urlname)

        self.assertEqual(url_path,'/dashboard/publishers/')
    
    def test_publisher_detail_url(self):
        urlname = 'dashboard:publisher_detail'
        url_path = reverse(urlname,args=[1])

        self.assertEqual(url_path,'/dashboard/publisher/detail/1/')
    
    def test_publisher_create_url(self):
        urlname = 'dashboard:publisher_create'
        url_path = reverse(urlname)

        self.assertEqual(url_path,'/dashboard/publisher/create/')

    def test_publisher_update_url(self):
        urlname = 'dashboard:publisher_update'
        url_path = reverse(urlname,args=[1])

        self.assertEqual(url_path,'/dashboard/publisher/update/1/')
    
    def test_publisher_delete_url(self):
        urlname = 'dashboard:publisher_delete'
        url_path = reverse(urlname,args=[1])

        self.assertEqual(url_path,'/dashboard/publisher/delete/1/')
    
    def test_category_url(self):
        urlname = 'dashboard:category_list'
        url_path = reverse(urlname)

        self.assertEqual(url_path,'/dashboard/categories/')
    
    def test_category_detail_url(self):
        urlname = 'dashboard:category_detail'
        url_path = reverse(urlname,args=[1])

        self.assertEqual(url_path,'/dashboard/category/detail/1/')
    
    def test_category_create_url(self):
        urlname = 'dashboard:category_create'
        url_path = reverse(urlname)

        self.assertEqual(url_path,'/dashboard/category/create/')
    
    def test_category_update_url(self):
        urlname = 'dashboard:category_update'
        url_path = reverse(urlname,args=[1])

        self.assertEqual(url_path,'/dashboard/category/update/1/')
    
    def test_category_delete_url(self):
        urlname = 'dashboard:category_delete'
        url_path = reverse(urlname,args=[1])

        self.assertEqual(url_path,'/dashboard/category/delete/1/')
    
    def test_book_url(self):
        urlname = 'dashboard:book_list'
        urlpath = reverse(urlname)

        self.assertEqual(urlpath,'/dashboard/books/')
    
    def test_book_detail_url(self):
        urlname = 'dashboard:book_detail'
        urlpath = reverse(urlname,args=['test'])

        self.assertEqual(urlpath,'/dashboard/book/detail/test/')
    
    def test_book_create_url(self):
        urlname = 'dashboard:book_create'
        urlpath = reverse(urlname)

        self.assertEqual(urlpath,'/dashboard/book/create/')
    
    def test_book_update_url(self):
        urlname = 'dashboard:book_update'
        urlpath = reverse(urlname,args=['test'])

        self.assertEqual(urlpath,'/dashboard/book/update/test/')
    
    def test_book_delete_url(self):
        urlname = 'dashboard:book_delete'
        urlpath = reverse(urlname,args=['test'])

        self.assertEqual(urlpath,'/dashboard/book/delete/test/')
    
    def test_book_copy_url(self):
        urlname = 'dashboard:book_copy_list'
        urlpath = reverse(urlname)

        self.assertEqual(urlpath,'/dashboard/book_copy/')
    
    def test_book_copy_detail_url(self):
        urlname = 'dashboard:book_copy_detail'
        urlpath = reverse(urlname,args=[1])

        self.assertEqual(urlpath,'/dashboard/book_copy/detail/1/')
    
    def test_book_copy_create_url(self):
        urlname = 'dashboard:book_copy_create'
        urlpath = reverse(urlname)

        self.assertEqual(urlpath,'/dashboard/book_copy/create/')
    
    def test_book_copy_update_url(self):
        urlname = 'dashboard:book_copy_update'
        urlpath = reverse(urlname,args=[1])

        self.assertEqual(urlpath,'/dashboard/book_copy/update/1/')
    
    def test_book_copy_delete_url(self):
        urlname = 'dashboard:book_copy_delete'
        urlpath = reverse(urlname,args=[1])

        self.assertEqual(urlpath,'/dashboard/book_copy/delete/1/')

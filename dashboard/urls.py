from django.urls import path

from dashboard.views.author_views import (
    AuthorListView,AuthorDetailView,AuthorCreateView,AuthorUpdateView,AuthorDeleteView
)
from dashboard.views.publisher_views import (
    PublisherListView,PublisherDetailView,PublisherCreateView,PublisherUpdateView,
    PublisherDeleteView
)
from dashboard.views.category_views import (
    CategoryListView,CategoryDetailView,CategoryCreateView,CategoryUpdateView,CategoryDeleteView
)
from dashboard.views.book_views import (
    BookListView,BookDetailView,BookCreateView,BookUpdateView,BookDeleteView
)
from dashboard.views.book_copy_views import (
    BookCopyListView,BookCopyDetailView,BookCopyCreateView,BookCopyUpdateView,
    BookCopyDeleteView
)

from dashboard.views.dashboard_views import (
    DashboardView
)

app_name = 'dashboard'

urlpatterns = [
    # Dashboard
    path('',DashboardView.as_view(),name='dashboard'),
    
    # Author urls
    path('authors/',AuthorListView.as_view(),name='author_list'),
    path('author/detail/<int:pk>/',AuthorDetailView.as_view(),name='author_detail'),
    path('author/create/',AuthorCreateView.as_view(),name='author_create'),
    path('author/update/<int:pk>/',AuthorUpdateView.as_view(),name='author_update'),
    path('author/delete/<int:pk>/',AuthorDeleteView.as_view(),name='author_delete'),

    # Publisher urls
    path('publishers/',PublisherListView.as_view(),name='publisher_list'),
    path('publisher/detail/<int:pk>/',PublisherDetailView.as_view(),name='publisher_detail'),
    path('publisher/create/',PublisherCreateView.as_view(),name='publisher_create'),
    path('publisher/update/<int:pk>/',PublisherUpdateView.as_view(),name='publisher_update'),
    path('publisher/delete/<int:pk>/',PublisherDeleteView.as_view(),name='publisher_delete'),

    # Category urls
    path('categories/',CategoryListView.as_view(),name='category_list'),
    path('category/detail/<int:pk>/',CategoryDetailView.as_view(),name='category_detail'),
    path('category/create/',CategoryCreateView.as_view(),name='category_create'),
    path('category/update/<int:pk>/',CategoryUpdateView.as_view(),name='category_update'),
    path('category/delete/<int:pk>/',CategoryDeleteView.as_view(),name='category_delete'),

    # Book urls
    path('books/',BookListView.as_view(),name='book_list'),
    path('book/detail/<slug:slug>/',BookDetailView.as_view(),name='book_detail'),
    path('book/create/',BookCreateView.as_view(),name='book_create'),
    path('book/update/<slug:slug>/',BookUpdateView.as_view(),name='book_update'),
    path('book/delete/<slug:slug>/',BookDeleteView.as_view(),name='book_delete'),

    # Book Copy urls
    path('book_copy/',BookCopyListView.as_view(),name='book_copy_list'),
    path('book_copy/detail/<int:pk>/',BookCopyDetailView.as_view(),name='book_copy_detail'),
    path('book_copy/create/',BookCopyCreateView.as_view(),name='book_copy_create'),
    path('book_copy/update/<int:pk>/',BookCopyUpdateView.as_view(),name='book_copy_update'),
    path('book_copy/delete/<int:pk>/',BookCopyDeleteView.as_view(),name='book_copy_delete')
]
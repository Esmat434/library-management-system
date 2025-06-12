from django.urls import path

from .views import (
    BookListView,BookDetailView,BookFilterByAuthorView,BookFilterByCategoryView,
    BookFilterByPublisherView,BorrowTransactionListView,BorrowTransactionCreateView,ReservedListView,
    ReservationCreateView,ReturnBorrowView
)

app_name = 'books'

urlpatterns = [
    # Book Views
    path('books/',BookListView.as_view(),name='home'),
    path('books/<slug:slug>/',BookDetailView.as_view(),name='book_detail'),
    
    # Filters
    path('books/filter/author/',BookFilterByAuthorView.as_view(),name='book_filter_by_author'),
    path('books/filter/category/',BookFilterByCategoryView.as_view(),name='book_filter_by_category'),
    path('books/filter/publisher/',BookFilterByPublisherView.as_view(),name='book_filter_by_publisher'),
    
    # Borrow Transaction
    path('borrow/',BorrowTransactionListView.as_view(),name='borrow_transaction_list'),
    path('borrow/<slug:slug>/',BorrowTransactionCreateView.as_view(),name='borrow_transaction_create'),
    
    # Reservations
    path('reserved/',ReservedListView.as_view(),name='reserved_list'),
    path('reserved/<slug:slug>/',ReservationCreateView.as_view(),name='reserved_create'),
    
    # Return Borrow
    path('return_borrow/<int:pk>/',ReturnBorrowView.as_view(),name='return_borrow'),
]
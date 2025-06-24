from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseNotFound,HttpResponseBadRequest
from django.views import View
from django.contrib import messages
from django.db import transaction,IntegrityError
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.utils.timezone import now
from datetime import timedelta

from .mixins import (
    LoginRequiredMixin
)

from .models import (
    Book,Category,Author,Publisher,BookCopy,BorrowTransaction,Reservation,Fine
)
# Create your views here.

class BookListView(View):
    def get(self,request):
        books = self.get_paginator(request)
        categories = Category.objects.filter(books__isnull=False).distinct()
        authors = Author.objects.filter(books__isnull=False).distinct()
        publishers = Publisher.objects.filter(books__isnull=False).distinct()
        return render(
            request,
            'books/book_list.html',
            {'books':books,'categories':categories,'authors':authors,'publishers':publishers}
            )

    def get_paginator(self,request):
        books = Book.objects.all().order_by('id')
        
        paginator = Paginator(books,12)

        page_number = request.GET.get('page')

        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.get_page(1)
        except EmptyPage:
            page_obj = paginator.get_page(paginator.num_pages)
        
        return page_obj

class BookDetailView(View):
    def get(self,request,slug):
        book = get_object_or_404(Book,slug = slug)
        book_copy = BookCopy.objects.filter(book = book,status='available')
        return render(request,'books/book_detail.html',{'book':book,'book_copy':book_copy})

# Helper Function For Filtering
def filter_books_by(request,model,filter_name,attr_name,tamplate_name='books/book_list.html'):
    query = request.GET.get(filter_name,'')
    obj = get_object_or_404(model,**{attr_name:query})
    books = obj.books.all()
    categories = Category.objects.filter(books__isnull=False).distinct()
    authors = Author.objects.filter(books__isnull=False).distinct()
    publishers = Publisher.objects.filter(books__isnull=False).distinct()
    return render(request,tamplate_name,{'books':books,'categories':categories,'authors':authors
                                        ,'publishers':publishers})

class BookFilterByCategoryView(View):
    def get(self,request):
        return filter_books_by(request,Category,'category','name')

class BookFilterByAuthorView(View):
    def get(self,request):
        return filter_books_by(request,Author,'author','username')
        
class BookFilterByPublisherView(View):
    def get(self,request):
        return filter_books_by(request,Publisher,'publisher','username')

class BookSearch(View):
    def get(self,request):
        q = request.GET.get('q','')
        categories = Category.objects.filter(books__isnull=False).distinct()
        authors = Author.objects.filter(books__isnull=False).distinct()
        publishers = Publisher.objects.filter(books__isnull=False).distinct()
        if not q:
            books = Book.objects.all().order_by('id')
            books = self.get_paginator(request,books)
            return render(request,'books/book_list.html',{'books':books,'categories':categories,
                                                          'authors':authors,'publishers':publishers})
        
        books = Book.objects.filter(Q(title__icontains=q)|Q(description__icontains=q)).order_by('id')
        books = self.get_paginator(request,books)
        
        return render(request,'books/book_list.html',{'books':books,'categories':categories,
                                                      'authors':authors,'publishers':publishers})
    
    def get_paginator(self,request,books):
        paginator = Paginator(books,10)

        page_number = request.GET.get('page')

        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.get_page(1)
        except EmptyPage:
            page_obj = paginator.get_page(paginator.num_pages)
        
        return page_obj

class BorrowTransactionListView(LoginRequiredMixin,View):
    def get(self,request):
        borrows = BorrowTransaction.objects.filter(user = request.user)
        return render(request,'books/borrow_transaction_list.html',{'borrows':borrows})

class BorrowTransactionCreateView(LoginRequiredMixin, View):
    def post(self, request, slug):
        book, book_copy = self.get_book_and_copy(slug, request.POST.get("q"))

        if not self.is_copy_available(book_copy):
            return HttpResponseNotFound("This book copy is not available.")

        if self.has_active_transaction(request.user, book_copy):
            messages.error(request, "You have already borrowed this book copy.")
            return redirect("books:borrow_transaction_list")

        if self.reuse_returned_transaction(request.user, book_copy):
            self.cleanup_after_borrow(request.user, book, book_copy)
            messages.success(request, "You have successfully borrowed this book copy again.")
            return redirect("books:borrow_transaction_list")

        try:
            with transaction.atomic():
                self.create_new_transaction(request.user, book_copy)
                self.cleanup_after_borrow(request.user, book, book_copy)
                messages.success(request, "This Book Successfully Borrowed.")
        except IntegrityError:
            messages.error(request, "This borrow transaction already exists.")

        return redirect("books:borrow_transaction_list")

    # ----------------------------
    # Helper Methods
    # ----------------------------

    def get_book_and_copy(self, slug, copy_number):
        book = get_object_or_404(Book, slug=slug)
        book_copy = get_object_or_404(BookCopy, book=book, copy_number=copy_number)
        return book, book_copy

    def is_copy_available(self, book_copy):
        return book_copy.status in ['available', 'reserved']

    def has_active_transaction(self, user, book_copy):
        return BorrowTransaction.objects.filter(
            user=user,
            book_copy=book_copy,
            is_returned=False
        ).exists()

    def reuse_returned_transaction(self, user, book_copy):
        transaction = BorrowTransaction.objects.filter(
            user=user,
            book_copy=book_copy,
            is_returned=True
        ).first()

        if transaction:
            transaction.is_returned = False
            transaction.due_date = now() + timedelta(days=10)
            transaction.save()
            return True
        return False

    def create_new_transaction(self, user, book_copy):
        BorrowTransaction.objects.create(
            user=user,
            book_copy=book_copy,
            due_date=now() + timedelta(days=10)
        )

    def cleanup_after_borrow(self, user, book, book_copy):
        book_copy.status = 'borrowed'
        book_copy.save()

        book.available_copies -= 1
        book.save()

        Reservation.objects.filter(user=user, book_copy=book_copy).delete()

class ReservedListView(LoginRequiredMixin,View):
    def get(self,request):
        reserve_books = Reservation.objects.filter(user = request.user)
        return render(request,'books/reserved_list.html',{'reserve_books':reserve_books})

class ReservationCreateView(LoginRequiredMixin,View):
    def post(self,request,slug):
        copy_number = request.POST.get('q')
        
        book = get_object_or_404(Book, slug=slug)

        book_copy = get_object_or_404(BookCopy, book=book, copy_number=copy_number)

        # check if this book was reserved
        if Reservation.objects.filter(user=request.user, book_copy=book_copy, is_active=True).exists():
            messages.warning(request, 'You have already reserved this book copy.')
            return redirect('books:reserved_list')

        # check book status
        if book_copy.status != 'available':
            return HttpResponseBadRequest("This book copy is not available for reservation.")
        
        with transaction.atomic():

            Reservation.objects.create(
                user = request.user,
                book_copy = book_copy,
                is_active = True
            )

            # Update status
            book_copy.status = 'reserved'
            book_copy.save()

        messages.success(request,'This Book was Successfully Reserved.')
        return redirect('books:reserved_list')

class ReturnBorrowView(LoginRequiredMixin,View):
    def post(self,request,pk):
        borrow_transaction = get_object_or_404(BorrowTransaction, id=pk, user=request.user,is_returned=False)

        with transaction.atomic():
            
            # Update status
            borrow_transaction.book_copy.status = 'available'
            borrow_transaction.book_copy.save()

            # Increase available copies
            borrow_transaction.book_copy.book.available_copies+=1
            borrow_transaction.book_copy.book.save()

            # Fine calculation
            per_day_fine_amount = 100
            overdue_days = (now().date() - borrow_transaction.due_date).days
            
            if overdue_days > 0:
                fine_amount = overdue_days * per_day_fine_amount

                borrow_transaction.fine_amount = fine_amount
                borrow_transaction.save()

                Fine.objects.create(
                    user=request.user,
                    borrow_transaction=borrow_transaction,
                    amount=fine_amount,
                    is_paid=True
                )

            borrow_transaction.is_returned = True
            borrow_transaction.save()

        messages.success(request,'This book was successfully delivered.')
        return redirect('books:borrow_transaction_list') 
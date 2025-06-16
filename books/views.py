from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseNotFound,HttpResponseBadRequest
from django.views import View
from django.contrib import messages
from django.db import transaction
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
        books = Book.objects.all()
        return render(request,'books/book_list.html',{'books':books})

class BookDetailView(View):
    def get(self,request,slug):
        book = get_object_or_404(Book,slug = slug)
        book_copy = BookCopy.objects.filter(book = book,status = 'available')
        return render(request,'books/book_detail.html',{'book':book,'book_copy':book_copy})

# Helper Function For Filtering
def filter_books_by(request,model,attr_name,tamplate_name='books/book_list.html'):
    query = request.GET.get('q','')
    obj = get_object_or_404(model,**{attr_name:query})
    books = obj.books.all()
    return render(request,tamplate_name,{'books':books})

class BookFilterByCategoryView(View):
    def get(self,request):
        return filter_books_by(request,Category,'name')

class BookFilterByAuthorView(View):
    def get(self,request):
        return filter_books_by(request,Author,'username')
        
class BookFilterByPublisherView(View):
    def get(self,request):
        return filter_books_by(request,Publisher,'username')

class BorrowTransactionListView(LoginRequiredMixin,View):
    def get(self,request):
        borrows = BorrowTransaction.objects.filter(user = request.user,is_returned=False)
        return render(request,'books/borrow_transaction_list.html',{'borrows':borrows})

class BorrowTransactionCreateView(LoginRequiredMixin,View):
    def post(self,request,slug):
        copy_number = request.POST.get('q')

        book = get_object_or_404(Book, slug=slug)

        book_copy = get_object_or_404(BookCopy, book=book, copy_number=copy_number)

        if book_copy.status != 'available':
            return HttpResponseNotFound("This book copy is not available.")
        
        with transaction.atomic():
            BorrowTransaction.objects.create(
                user = request.user,
                book_copy = book_copy,
                due_date = now() + timedelta(days=10)
            )

            # Update status
            book_copy.status = 'borrowed'
            book_copy.save()

            # Decrease available copies
            book.available_copies-=1
            book.save()

            # Delete Reservation is it exists
            Reservation.objects.filter(user=request.user, book_copy=book_copy).delete()

        messages.success(request,'This Book Successfully Borrowed.')
        return redirect('books:borrow_transaction_list')

class ReservedListView(LoginRequiredMixin,View):
    def get(self,request):
        books = Reservation.objects.filter(user = request.user)
        return render(request,'books/reserved_list.html',{'books':books})

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
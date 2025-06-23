from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.urls import reverse
from django.contrib import messages

from books.models import (
    Book,BookCopy
)

from dashboard.forms.book_forms import (
    BookCreationForm,BookUpdateForm
)

from dashboard.mixins import (
    LoginRequiredMixin,RoleCheckMixin
)

class BookListView(LoginRequiredMixin,RoleCheckMixin,View):
    def get(self,request):
        books = Book.objects.all()
        return render(request,'dashboard/book_list.html',{'books':books})

class BookDetailView(LoginRequiredMixin,RoleCheckMixin,View):
    def get(self,request,slug):
        book = get_object_or_404(Book, slug=slug)
        return render(request,'dashboard/book_detail.html',{'book':book})

class BookCreateView(LoginRequiredMixin,RoleCheckMixin,View):
    def get(self,request):
        form = BookCreationForm()
        return render(request,'dashboard/book_create.html',{'form':form})

    def post(self,request):
        form = BookCreationForm(request.POST,request.FILES)
        print(form.errors)
        if form.is_valid():
            form.save()
            messages.success(request,'Your book successfully created.')
            return redirect('dashboard:book_list')
        else:
            messages.error(request,'Your data was invalid.')
            return render(request,'dashboard/book_create.html',{'form':form})

class BookUpdateView(LoginRequiredMixin,RoleCheckMixin,View):
    def get(self,request,slug):
        book = get_object_or_404(Book,slug=slug)
        form = BookUpdateForm(instance=book)
        return render(request,'dashboard/book_update.html',{'form':form})
    
    def post(self,request,slug):
        book = get_object_or_404(Book,slug=slug)
        form = BookUpdateForm(request.POST,request.FILES,instance=book)
        print(form.errors)
        if form.is_valid():
            form.save()
            messages.success(request,'This book successfully updated.')
            return redirect(reverse('dashboard:book_detail',args=[form.instance.slug]))
        else:
            messages.error(request,'Your data was invalid.')
            return render(request,'dashboard/book_update.html',{'form':form})

class BookDeleteView(LoginRequiredMixin,RoleCheckMixin,View):
    def post(self,request,slug):
        book = get_object_or_404(Book, slug=slug)

        if BookCopy.objects.filter(book=book).exists():
            messages.error(request,'The Book Copy of this book exists delete that before delete this')
            return redirect(reverse('dashboard:book_detail'))
        
        book.delete()

        return redirect('dashboard:book_list')
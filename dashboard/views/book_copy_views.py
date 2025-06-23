from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.views import View
from django.contrib import messages

from books.models import (
    BookCopy,BorrowTransaction,Reservation
)

from dashboard.forms.book_copy_forms import (
    BookCopyCreationForm,BookCopyUpdateForm
)

from dashboard.mixins import (
    LoginRequiredMixin,RoleCheckMixin
)

class BookCopyListView(LoginRequiredMixin,RoleCheckMixin,View):
    def get(self,request):
        book_copy = BookCopy.objects.all()
        return render(request,'dashboard/book_copy_list.html',{'book_copy':book_copy})

class BookCopyDetailView(LoginRequiredMixin,RoleCheckMixin,View):
    def get(self,request,pk):
        book_copy = get_object_or_404(BookCopy, id=pk)
        return render(request,'dashboard/book_copy_detail.html',{'book_copy':book_copy})

class BookCopyCreateView(LoginRequiredMixin,RoleCheckMixin,View):
    def get(self,request):
        form = BookCopyCreationForm()
        return render(request,'dashboard/book_copy_create.html',{'form':form})
    
    def post(self,request):
        form = BookCopyCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Book Copy successfully created.')
            return redirect('dashboard:book_copy_list')
        else:
            messages.error(request,'Your data was invalid.')
            return render(request,'dashboard/book_copy_create.html',{'form':form})

class BookCopyUpdateView(LoginRequiredMixin,RoleCheckMixin,View):
    def get(self,request,pk):
        book_copy = get_object_or_404(BookCopy, id=pk)
        form = BookCopyUpdateForm(instance=book_copy)
        return render(request,'dashboard/book_copy_update.html',{'form':form})
    
    def post(self,request,pk):
        book_copy = get_object_or_404(BookCopy, id=pk)
        form = BookCopyUpdateForm(request.POST,instance=book_copy)
        if form.is_valid():
            form.save()
            messages.success(request,'Your book copy successfully updated.')
            return redirect(reverse('dashboard:book_copy_detail',args=[pk]))
        else:
            messages.error(request,'Your data was invalid.')
            return render(request,'dashboard/book_copy_detail.html',{'form':form})

class BookCopyDeleteView(LoginRequiredMixin,RoleCheckMixin,View):
    def post(self,request,pk):
        book_copy = get_object_or_404(BookCopy, id=pk)

        if BorrowTransaction.objects.filter(book_copy=book_copy).exists():
            messages.error(
                request,
                'This book copy is linked to one or more borrow transactions. Please delete those transactions before deleting this copy.'
            )
            return redirect(reverse('dashboard:book_copy_detail',args=[pk]))
        
        if Reservation.objects.filter(book_copy=book_copy).exists():
            messages.error(request,'This book copy data exists in reservation delete that before delete this book copy.')
            return redirect(reverse('dashboard:book_copy_detail',args=[pk]))
        
        book_copy.delete()
        messages.success(request,"Your book copy successfully deleted.")
        return redirect('dashboard:book_copy_list')
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.views import View

from books.models import (
    Author,Book
)

from dashboard.forms.author_forms import (
    AuthorCreationForm,AuthorUpdateForm
)

from dashboard.mixins import (
    LoginRequiredMixin,RoleCheckMixin
)

class AuthorListView(LoginRequiredMixin,RoleCheckMixin,View):
    def get(self,request):
        authors = Author.objects.all()
        return render(request,'dashboard/author_list.html',{'authors':authors})
    
class AuthorDetailView(LoginRequiredMixin,RoleCheckMixin,View):
    def get(self,request,pk):
        author = get_object_or_404(Author, id=pk)
        return render(request,'dashboard/author_detail.html',{'author':author})

class AuthorCreateView(LoginRequiredMixin,RoleCheckMixin,View):
    def get(self,request):
        form = AuthorCreationForm()
        return render(request,'dashboard/author_create.html',{'form':form})
    
    def post(self,request):
        form = AuthorCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Your author successfully created.')
            return redirect('dashboard:author_list')
        else:
            messages.error(request,'Your data was invalid.')
            return render(request,'dashboard/book_create.html',{'form':form})

class AuthorUpdateView(LoginRequiredMixin,RoleCheckMixin,View):
    def get(self,request,pk):
        author = get_object_or_404(Author, id=pk)
        form = AuthorUpdateForm(instance=author)
        return render(request,'dashboard/author_update.html',{'form':form})
    
    def post(self,request,pk):
        author = get_object_or_404(Author, id=pk)
        form = AuthorUpdateForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            messages.success(request,'Your author successfully updated.')
            return redirect(reverse('dashboard:author_detail',args=[pk]))
        else:
            messages.error(request,'Your data was invalid.')
            return render(request,'dashboard/author_update.html',{'form':form})

class AuthorDeleteView(LoginRequiredMixin,RoleCheckMixin,View):
    def post(self,request,pk):
        author = get_object_or_404(Author, id=pk)

        if Book.objects.filter(author=author).exists():
            messages.error(request,'This author exists in Book delete that before delete this author.')
            return redirect(reverse('dashboard:author_detail',args=[pk]))
        
        author.delete()
        messages.success(request,'your author successfully deleted.')
        return redirect('dashboard:author_list')

from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.views import View

from books.models import (
    Category,Book
)

from dashboard.forms.category_forms import (
    CategoryCreationForm,CategoryUpdateForm
)

from dashboard.mixins import (
    LoginRequiredMixin,RoleCheckMixin
)

class CategoryListView(LoginRequiredMixin,RoleCheckMixin,View):
    def get(self,request):
        categories = Category.objects.all()
        return render(request,'dashboard/category_list.html',{'categories':categories})

class CategoryDetailView(LoginRequiredMixin,RoleCheckMixin,View):
    def get(self,request,pk):
        category = get_object_or_404(Category, id=pk)
        return render(request,'dashboard/category_detail.html',{'category':category})

class CategoryCreateView(LoginRequiredMixin,RoleCheckMixin,View):
    def get(self,request):
        form = CategoryCreationForm()
        return render(request,'dashboard/category_create.html',{'form':form})
    
    def post(self,request):
        form = CategoryCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Your category successfully created.')
            return redirect('dashboard:category_list')
        else:
            messages.error(request,'Your data was invalid.')
            return render(request,'dashboard/category_create.html',{'form':form})

class CategoryUpdateView(LoginRequiredMixin,RoleCheckMixin,View):
    def get(self,request,pk):
        category = get_object_or_404(Category, id=pk)
        form = CategoryUpdateForm(instance=category)
        return render(request,'dashboard/category_update.html',{'form':form})
    
    def post(self,request,pk):
        category = get_object_or_404(Category, id=pk)
        form = CategoryUpdateForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request,'Your category successfully updated.')
            return redirect(reverse('dashboard:category_detail',args=[pk]))
        else:
            messages.error(request,'Your data was invalid.')
            return render(request,'dashboard/category_update.html',{'form':form})

class CategoryDeleteView(LoginRequiredMixin,RoleCheckMixin,View):
    def post(self,request,pk):
        category = get_object_or_404(Category, id=pk)

        if Book.objects.filter(category=category).exists():
            messages.error(request,'please delete book of this category before delete category.')
            return redirect(reverse('dashboard:category_detail',args=[pk]))
        
        category.delete()
        messages.success(request,'Your category successfully deleted.')
        return redirect('dashboard:category_list')
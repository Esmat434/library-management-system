from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.views import View

from books.models import (
    Publisher,Book
)

from dashboard.forms.publisher_forms import (
    PublisherCreationForm,PublisherUpdateForm
)

from dashboard.mixins import (
    LoginRequiredMixin,RoleCheckMixin
)

class PublisherListView(LoginRequiredMixin,RoleCheckMixin,View):
    def get(self,request):
        publishers = Publisher.objects.all()
        return render(request,'dashboard/publisher_list.html',{'publishers':publishers})

class PublisherDetailView(LoginRequiredMixin,RoleCheckMixin,View):
    def get(self,request,pk):
        publisher = get_object_or_404(Publisher, id=pk)
        return render(request,'dashboard/publisher_detail.html',{'publisher':publisher})

class PublisherCreateView(LoginRequiredMixin,RoleCheckMixin,View):
    def get(self,request):
        form = PublisherCreationForm()
        return render(request,'dashboard/publisher_create.html',{'form':form})
    
    def post(self,request):
        form = PublisherCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Your publisher successfully created.')
            return redirect('dashboard:publisher_list')
        else:
            messages.error(request,'Your data was invalid.')
            return render(request,'dashboard/publisher_create.html',{'form':form})
        
class PublisherUpdateView(LoginRequiredMixin,RoleCheckMixin,View):
    def get(self,request,pk):
        publisher = get_object_or_404(Publisher, id=pk)
        form = PublisherUpdateForm(instance=publisher)
        return render(request,'dashboard/publisher_update.html',{'form':form})
    
    def post(self,request,pk):
        publisher = get_object_or_404(Publisher, id=pk)
        form = PublisherUpdateForm(request.POST, instance=publisher)
        if form.is_valid():
            form.save()
            messages.success(request,'Your publisher was successfully updated.')
            return redirect(reverse('dashboard:publisher_detail',args=[pk]))
        else:
            messages.error(request,'Your data was invalid.')
            return render(request,'dashboard/publisher_update.html',{'form':form})

class PublisherDeleteView(LoginRequiredMixin,RoleCheckMixin,View):
    def post(self,request,pk):
        publisher = get_object_or_404(Publisher, id=pk)

        if Book.objects.filter(publisher=publisher).exists():
            messages.error(request,'delete the book of this publisher before delete publisher.')
            return redirect(reverse('dashboard:publisher_detail',args=[pk]))
        
        publisher.delete()
        messages.success(request,'Your publisher sucessfully deleted.')
        return redirect('dashboard:publisher_list')
    
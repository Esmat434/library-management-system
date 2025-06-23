from django.shortcuts import render,redirect
from django.contrib import messages
from django.views import View

from .forms import (
    ContactCreationForm
)

# Create your views here.

class AboutUsView(View):
    def get(self,request):
        return render(request,'core/about_us.html')

class ContactUsView(View):
    def get(self,request):
        form = ContactCreationForm()
        return render(request,'core/contact_us.html',{'form':form})
    
    def post(self,request):
        form = ContactCreationForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user if request.user.is_authenticated else None
            contact.save()
            messages.success(request,'Your contact message successfully sended.')
            return redirect('books:home')
        messages.error(request,'Your data was invalid.')
        return render(request,'core/contact_us.html')
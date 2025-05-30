from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.mixins import AccessMixin

class LoginRequiredMixin(AccessMixin):
    def dispatch(self,request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('accounts:login'))
        return super().dispatch(request,*args,**kwargs)

class LogoutRequiredMixin(AccessMixin):
    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request,*args,**kwargs)

class AccountVerifiedMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not getattr(request.user,'email_verified',False):
            return render(request,'accounts/account_verified_message.html')
        return super().dispatch(request, *args, **kwargs)
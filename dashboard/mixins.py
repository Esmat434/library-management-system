from django.shortcuts import redirect
from django.http import HttpResponseNotFound
from django.urls import reverse
from django.contrib.auth.mixins import AccessMixin

class LoginRequiredMixin(AccessMixin):
    def dispatch(self,request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('accounts:login'))
        return super().dispatch(request,*args,**kwargs)

class RoleCheckMixin(AccessMixin):
    def dispatch(self,request,*args,**kwargs):
        if request.user.role not in ['admin', 'librarian']:
            return HttpResponseNotFound('Access is denied.')
        
        return super().dispatch(request,*args,**kwargs)
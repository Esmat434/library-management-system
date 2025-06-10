from django.urls import reverse_lazy
from django.contrib.auth.mixins import AccessMixin

class LoginRequiredMixin(AccessMixin):
    login_url = reverse_lazy('accounts:login')
    permission_denied_message = 'You must login before'
    
    def dispatch(self,request,*args,**kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request,*args,**kwargs)
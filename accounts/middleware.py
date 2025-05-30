import time
from django.core.cache import cache
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

class LoginAttemptThrottleMiddleware(MiddlewareMixin):
    def __init__(self, get_response = ...):
        super().__init__(get_response)
        self.get_response = get_response
        self.login_url_path = str(reverse_lazy('accounts:login'))
        print("LoginAttemp Middleware.")
    
    def get_client_ip(self,request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def __call__(self, request):
        if request.method == 'POST' and request.path == self.login_url_path:
            ip_address = self.get_client_ip(request)
            username = request.POST.get('username')

            if not username:
                return self.get_response(request)
            
            lockout_cache_key = f'lockout_{ip_address}_{username}'

            is_locked = cache.get(lockout_cache_key)

            if is_locked:
                lockout_remaining_time_key = f'lockout_expiry_{ip_address}_{username}'
                expiry_time = cache.get(lockout_remaining_time_key,0)
                remaining_time = int(expiry_time - time.time())

                if remaining_time > 0:
                    return render(request,'accounts/login.html',{'login_locked':True,'remaining_time':remaining_time})
                else:
                    cache.delete(lockout_cache_key)
                    cache.delete(lockout_remaining_time_key)
                    attempt_count_key = f'login_attempts_{ip_address}_{username}'
                    cache.delete(attempt_count_key)

            response = self.get_response(request)
            
            return response

class MaintenanceModeMiddleware(MiddlewareMixin):
    def __init__(self, get_response = ...):
        super().__init__(get_response)
        self.get_response = get_response
    
    def __call__(self, request):
        if settings.MAINTENANCE_MODE:
            return render(request,'maintenance.html')
        response = self.get_response(request)
        return response
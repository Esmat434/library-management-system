import uuid
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render,redirect
from django.http import Http404,HttpResponseNotFound
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate,update_session_auth_hash
from django.views import View

from .mixins import (
    LoginRequiredMixin,LogoutRequiredMixin,AccountVerifiedMixin
)

from .forms import (
    UserForm,UserUpdateForm,ChangePasswordForm,ForgotPasswordForm
)

from .models import (
    CustomUser,AccountVerificationToken,ChangePasswordToken,ForgotPasswordToken
)

class RegisterView(LogoutRequiredMixin,View):
    def get(self,request):
        form = UserForm()
        return render(request,'accounts/register.html',{'form':form})

    def post(self,request):
        form = UserForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Your registration was successful. Please log in to continue.')
            return render(request,'accounts/account_verified_message.html')
        return render(request,'accounts/register.html',{'form':form})    

class AccountVerifiedTokenView(LogoutRequiredMixin,View):
    def get(self,request,token):
        token_instance = self.check_token(token)
        if token_instance:
            user_to_verify = token_instance.user
            
            if hasattr(user_to_verify,'email_verified') and user_to_verify.email_verified:
                messages.info(request,'Your email has already been verified.')
                return redirect('accounts:login')
            
            if hasattr(user_to_verify,'email_verified'):
                user_to_verify.email_verified = True
                user_to_verify.save(update_fields=['email_verified'])

            token_instance.delete()

            messages.success(request,"Your email has been successfully verified. You can now log in.")
            return redirect('accounts:login')
        else:

            messages.error(request,'The verification link is invalid or expired.')

            return HttpResponseNotFound("The verification link is invalid or expired.")
    
    def check_token(self,token):
        try:

            token_obj = AccountVerificationToken.objects.get(token = token)
            
            if hasattr(token_obj,'is_expired') and token_obj.is_expired():
                return None
            
            return token_obj
        except ChangePasswordToken.DoesNotExist:
            return None

class ResendAccountVerifiedTokenView(LogoutRequiredMixin,View):
    
    def get(self,request):
        return render(request,'resend_account_verified_token.html')
    
    def post(self,request):
        email = request.POST.get('email')
        new_token_val = uuid.uuid4()
        new_expiry_val = timezone.now() + timedelta(hours=24)
        try:
            user = CustomUser.objects.get(email = email)
            AccountVerificationToken.objects.update_or_create(
                user = user,
                defaults={
                    'token':new_token_val,
                    'expires_at':new_expiry_val
                }
            )
            return render(request,'accounts/account_verified_message.html')
        except CustomUser.DoesNotExist:
            return HttpResponseNotFound("Your email is incorrect")


class LoginView(AccountVerifiedMixin,View):
    def get(self,request):
        return render(request,'accounts/login.html')
    
    def post(self,request):
        data = request.POST
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request,username = username,password = password)

        if user:
            login(request,user)
            
            return redirect('/')
        else:
            messages.error(request,'The username or password entered is incorrect.')
            return render(request,'accounts/login.html')

class LogoutView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'accounts/logout.html')
    
    def post(self,request):
        logout(request)
        return redirect('/')

class ProfileView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'accounts/profile.html',{'user':request.user})

class ProfileUpdateView(LoginRequiredMixin,View):
    def get(self,request):
        form = UserUpdateForm(instance=request.user)
        return render(request,'accounts/profile_update.html',{'form':form})
    
    def post(self,request):
        form = UserUpdateForm(request.POST,request.FILES,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
        return render(request,'accounts/profile_update.html',{'form':form})
    
class ChangePasswordTokenView(LoginRequiredMixin,View):
    def get(self,request):
        ChangePasswordToken.objects.get_or_create(user = request.user)
        return render(request,'accounts/change_password_token.html')
    
    def post(self,request):
        new_token_val = uuid.uuid4()
        new_expiry_val = timezone.now() + timedelta(hours=24)
        ChangePasswordToken.objects.update_or_create(
            user = request.user,
            defaults={
                'token':new_token_val,
                'expires_at':new_expiry_val
            }
        )
        return render(request,'accounts/change_password_token.html')

class ChangePasswordView(LoginRequiredMixin,View):
    def get(self,request,token):
        if not self.check_token(request,token):
            return HttpResponseNotFound("Token Does Not Exists.")
        form = ChangePasswordForm()
        return render(request,'accounts/change_password.html',{'token':token,'form':form})
    
    def post(self,request,token):
        token_val = self.check_token(request,token)
        if not token_val:
            return HttpResponseNotFound("Token Does Not Exists.")
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            request.user.set_password(form.cleaned_data['password1'])
            request.user.save()
            update_session_auth_hash(request,request.user)

            token_val.delete()
            
            return redirect('accounts:profile')
        else:
            messages.error(request,'Your password is incorrect.')
            return render(request,'accounts/change_password.html',{'token':token})

    def check_token(self,request,token):
        try:
            token_instance = ChangePasswordToken.objects.get(user = request.user,token = token)
            if hasattr(token_instance,'is_expired') and token_instance.is_expired():
                return None
            return token
        except ChangePasswordToken.DoesNotExist:
            return None

class ForgotPasswordTokenView(LogoutRequiredMixin,View):
    def get(self,request):
        return render(request,'accounts/forgot_password_token.html')
    
    def post(self,request):
        new_token_val = uuid.uuid4()
        new_expiry_at = timezone.now() + timedelta(hours=24)
        user = self.get_user(request)
        
        if not user:
            return HttpResponseNotFound("Your Email Does Not Correct.")
        
        ForgotPasswordToken.objects.update_or_create(
            user = user,
            defaults={
                'token':new_token_val,
                'expires_at':new_expiry_at
            }
        )
        return render(request,'accounts/forgot_password_token_message.html')
    
    def get_user(self,request):
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email = email)
            return user
        except CustomUser.DoesNotExist:
            return None
        
class ForgotPasswordView(LogoutRequiredMixin,View):
    def get(self,request,token):
        
        if not self.check_token(token):
            return HttpResponseNotFound("Your Token Does Not Exists.")
        
        form = ForgotPasswordForm()
        return render(request,'accounts/forgot_password.html',{'token':token,'form':form})
    
    def post(self,request,token):
        token_val = self.check_token(token)
        if not token_val:
            return HttpResponseNotFound("Your Token Does Not Exists.")
        
        form = ForgotPasswordForm(request)
        
        if form.is_valid():
            token.user.set_password(form.cleaned_data['password1'])
            token.user.save()

            token_val.delete()

            return redirect('accounts:login')
        else:
            messages.error(request,'Your password is incorrect.')
            return render(request,'accounts/forgot_password.html',{'form':form})
    
    def check_token(self,token):
        try:
            token_instance = ForgotPasswordToken.objects.get(token = token)
            if hasattr(token_instance,'is_expired') and token_instance.is_expired():
                return None
            return token
        except ForgotPasswordToken.DoesNotExist:
            return None
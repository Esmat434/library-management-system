from django import forms

from books.models import (
    Author
)

class AuthorCreationForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('username','email','first_name','last_name','age','address')
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter User Name'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter Email'}),
            'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter First Name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Last Name'}),
            'age':forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter age'}),
            'address':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Address'})
        }
    
    def validate_username(self):
        username = self.cleaned_data.get('username','')

        if not username:
            raise forms.ValidationError('Please Enter Username')
        
        if Author.objects.filter(username=username).exists():
            raise forms.ValidationError('This username already exists.')
        
        return username
    
    def validate_email(self):
        email = self.cleaned_data.get('email','')

        if not email:
            raise forms.ValidationError("Please Enter Your Email.")
        
        if Author.objects.filter(email=email).exists():
            raise forms.ValidationError("This email already exists.")

class AuthorUpdateForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('username','email','first_name','last_name','age','address')
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter User Name'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter Email'}),
            'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter First Name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Last Name'}),
            'age':forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter age'}),
            'address':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Address'})
        }
    
    def validate_username(self):
        username = self.cleaned_data.get('username','')

        if not username:
            raise forms.ValidationError('Please Enter Username')
        
        if Author.objects.filter(username=username).exclude(id=self.instance.pk).exists():
            raise forms.ValidationError('This username already exists.')
        
        return username
    
    def validate_email(self):
        email = self.cleaned_data.get('email','')

        if not email:
            raise forms.ValidationError("Please Enter Your Email.")
        
        if Author.objects.filter(email=email).exclude(id=self.instance.pk).exists():
            raise forms.ValidationError("This email already exists.")
from django import forms

from .models import (
    Contact
)

class ContactCreationForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('username','email','phone_number','title','message')
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Username.'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter Email.'}),
            'phone_number':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Phone Number.'}),
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Title.'}),
            'message':forms.Textarea(attrs={'class':'forms-control','placeholder':'Enter Message.'})
        }
from django import forms

from .models import (
    Contact
)

class ContactCreationForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('username','email','phone_number','title','message')
        widgets = {
            'username':forms.TextInput(attrs={'class':'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500','placeholder':'Enter Username.'}),
            'email':forms.EmailInput(attrs={'class':'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500','placeholder':'Enter Email.'}),
            'phone_number':forms.TextInput(attrs={'class':'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500','placeholder':'Enter Phone Number.'}),
            'title':forms.TextInput(attrs={'class':'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500','placeholder':'Enter Title.'}),
            'message':forms.Textarea(attrs={'class':'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500','placeholder':'Enter Message.'})
        }
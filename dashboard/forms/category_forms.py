from django import forms

from books.models import (
    Category
)

class CategoryCreationForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name','description')
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Name'}),
            'description':forms.Textarea(attrs={'class':'form-control','placeholder':'Enter Description'})
        }

class CategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name','description')
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Name'}),
            'description':forms.Textarea(attrs={'class':'form-control','placeholder':'Enter Description'})
        }
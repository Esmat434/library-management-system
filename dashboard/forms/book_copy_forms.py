from django import forms

from books.models import (
    BookCopy
)

class BookCopyCreationForm(forms.ModelForm):
    class Meta:
        model = BookCopy
        fields = ('book','copy_number','status','location')
        widgets = {
            'book':forms.Select(attrs={'class':'form-control','placeholder':'Select Book'}),
            'copy_number':forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter Copy Number'}),
            'status':forms.Select(attrs={'class':'form-control','placeholder':'Select Status'}),
            'location':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Location'})
        }
    
    def validate(self):
        cleaned_data = super().validate()

        book = cleaned_data.get('book','')
        copy_number = cleaned_data.get('copy_number','')

        if not book:
            raise forms.ValidationError("Please Select Your Book.")
        
        if not copy_number:
            raise forms.ValidationError("Please Enter Copy Number.")
        
        if BookCopy.objects.filter(book=book, copy_number=copy_number).exists():
            raise forms.ValidationError("This book with copy number already exists.")
        
        return cleaned_data

class BookCopyUpdateForm(forms.ModelForm):
    class Meta:
        model = BookCopy
        fields = ('book','copy_number','status','location')
        widgets = {
            'book':forms.Select(attrs={'class':'form-control','placeholder':'Select Book'}),
            'copy_number':forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter Copy Number'}),
            'status':forms.Select(attrs={'class':'form-control','placeholder':'Select Status'}),
            'location':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Location'})
        }
    
    def validate(self):
        cleaned_data = super().validate()

        book = cleaned_data.get('book','')
        copy_number = cleaned_data.get('copy_number','')

        if not book:
            raise forms.ValidationError("Please Select Your Book.")
        
        if not copy_number:
            raise forms.ValidationError("Please Enter Copy Number.")
        
        if BookCopy.objects.filter(book=book, copy_number=copy_number).exclude(id=self.instance.pk).exists():
            raise forms.ValidationError("This book with copy number already exists.")
        
        return cleaned_data
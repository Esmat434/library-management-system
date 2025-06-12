from django import forms

from books.models import (
    Book
)

class BookCreationForm(forms.ModelForm):
    class Meta:
        model = Book
        fields =('author','publisher','category','title','description','isbn','slug','avatar',
                  'total_copies','available_copies','published_date'       
                )
        widgets = {
            'author':forms.Select(attrs={'class':'form-control','placeholder':'Select Author'}),
            'publisher':forms.Select(attrs={'class':'form-control','placeholder':'Select Publihser'}),
            'category':forms.Select(attrs={'class':'form-control','placeholder':'Select Category'}),
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Title'}),
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Description'}),
            'isbn':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Isbn'}),
            'slug':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Slug'}),
            'avatar':forms.FileInput(attrs={'class':'form-control'}),
            'total_copies':forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter Total Copies'}),
            'available_copies':forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter Avialable Copies'}),
            'published_date':forms.DateInput(attrs={'class':'form-control','placeholder':'Enter Published Date'})
        }
    
    def validate_title(self):
        title = self.cleaned_data.get('title','')

        if not title:
            raise forms.ValidationError("Please Enter Title")

        if Book.objects.filter(title=title).exists():
            raise forms.ValidationError('Your title already exists.')

        return title
    
    def validate_isbn(self):
        isbn = self.cleaned_data.get('isbn','')

        if not isbn:
            raise forms.ValidationError("Please Enter Isbn.")

        if Book.objects.filter(isbn=isbn).exists():
            raise forms.ValidationError("Your isbn already exists.")
        
        return isbn
    
    def validate_slug(self):
        slug = self.cleaned_data.get('slug','')

        if not slug:
            raise forms.ValidationError("Please Enter Slug.")

        if Book.objects.filter(slug=slug).exists():
            raise forms.ValidationError("Your slug already exists.")
        
        return slug

class BookUpdateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields =('author','publisher','category','title','description','isbn','slug','avatar',
                  'total_copies','available_copies','published_date'       
                )
        widgets = {
            'author':forms.Select(attrs={'class':'form-control','placeholder':'Select Author'}),
            'publisher':forms.Select(attrs={'class':'form-control','placeholder':'Select Publihser'}),
            'category':forms.Select(attrs={'class':'form-control','placeholder':'Select Category'}),
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Title'}),
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Description'}),
            'isbn':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Isbn'}),
            'slug':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Slug'}),
            'avatar':forms.FileInput(attrs={'class':'form-control'}),
            'total_copies':forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter Total Copies'}),
            'available_copies':forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter Avialable Copies'}),
            'published_date':forms.DateInput(attrs={'class':'form-control','placeholder':'Enter Published Date'})
        }
    
    def validate_title(self):
        title = self.cleaned_data.get('title','')

        if not title:
            raise forms.ValidationError("Please Enter Title")

        if Book.objects.filter(title=title).exclude(id=self.instance.pk).exists():
            raise forms.ValidationError('Your title already exists.')

        return title

    def validate_isbn(self):
        isbn = self.cleaned_data.get('isbn','')

        if not isbn:
            raise forms.ValidationError("Please Enter Isbn.")

        if Book.objects.filter(isbn=isbn).exclude(id=self.instance.pk).exists():
            raise forms.ValidationError("Your isbn already exists.")

        return isbn
    
    def validate_slug(self):
        slug = self.cleaned_data.get('slug','')

        if not slug:
            raise forms.ValidationError("Please Enter Slug.")

        if Book.objects.filter(slug=slug).exclude(id=self.instance.pk).exists():
            raise forms.ValidationError("Your slug already exists.")
        
        return slug
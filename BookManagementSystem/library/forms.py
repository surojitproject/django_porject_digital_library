from django import forms
from .models import Book
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class AddUpdateBook(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['book_pic', 'book_name', 'author', 'book_type', 'price', 'rating']
        widgets = {
            
            'book_name':forms.TextInput(attrs={'placeholder':'Enter Book Name', }),
            'author':forms.TextInput(attrs={'placeholder':'Enter Author'}),
            'price':forms.NumberInput(attrs={'placeholder':'Enter price in Rs'}),
             
        }

class Userform(UserCreationForm):
    class Meta:
        model = User
        fields =  ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']
        widgets = {
            'username':forms.TextInput(attrs={'placeholder':'Enter user name', 'required':True }),
            'first_name':forms.TextInput(attrs={'placeholder':'Enter first name', 'required':False}),
            'last_name':forms.TextInput(attrs={'placeholder':'Enter last name', 'required':False}),
            'email':forms.EmailInput(attrs={'placeholder':'Enter your email address','required':True}),            
        }


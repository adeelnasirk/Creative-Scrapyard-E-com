from django.contrib.auth.forms import UserCreationForm
from .models import User, Seller, Customer, SellerProfile, Product
from django import forms

class UserRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields=[
            'email',
            'username',
            'password1',
            'password2',
        ]

class CustomerRegistrationForm(UserCreationForm):
    
    class Meta:
        model = Customer
        fields = [
            'email',
            'username',
            'password1',
            'password2',
        ]


class SellerRegistrationForm(UserCreationForm):

    class Meta:
        model = Seller
        fields = [
            'email',
            'username',
            'password1',
            'password2',
        ]

class SellerRegistrationForm2(forms.ModelForm):
    class Meta:
        model= SellerProfile
        fields=[
            'Company_name',
            'Warehose_location',
            'contact_number',
        ]



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields= '__all__'
        exclude = [
            'seller',
            'in_stock',
        ]
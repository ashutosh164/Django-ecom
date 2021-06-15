from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import ShippingAddress


class UserRegistrationsForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AddressForm(forms.Form):
    class Meta:
        model = ShippingAddress
        fields = '__all__'


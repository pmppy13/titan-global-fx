from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignUpForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=True)
    country = forms.CharField(max_length=100, required=True)
    username = forms.CharField(max_length=150, required=True)
    security_pin = forms.CharField(max_length=6, required=True, widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('full_name', 'email', 'phone', 'country', 'username', 'security_pin', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        full_name = self.cleaned_data['full_name'].strip()
        name_parts = full_name.split()
        user.first_name = name_parts[0] if name_parts else ''
        user.last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        user.country = self.cleaned_data['country']
        user.security_pin = self.cleaned_data['security_pin']
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False)
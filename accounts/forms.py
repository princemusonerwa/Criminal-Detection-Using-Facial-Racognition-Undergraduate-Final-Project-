from django import forms 
from .models import User, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ('names', 'email','phone', 'gender', 'dob', 'address')
    
        widgets = {
                'names' : forms.TextInput(attrs={'class': 'form-control'}),
                'email' : forms.TextInput(attrs={'class': 'form-control'}),
                'phone' : forms.TextInput(attrs={'class': 'form-control'}),
                'gender' : forms.TextInput(attrs={'class': 'form-control'}),
                'gender' : forms.TextInput(attrs={'class': 'form-control'}),
                'dob' : forms.TextInput(attrs={'class': 'form-control'}),
                'address' : forms.TextInput(attrs={'class': 'form-control'}),         
            }
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['names','email', 'phone', 'gender', 'dob', 'address']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
    
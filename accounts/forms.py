from django import forms
from requests import request
from .models import *
# import authenicate
from django.contrib.auth import authenticate, login
from django.contrib import messages


class DoctorRegistrationForm(forms.ModelForm):
    class Meta:
        model = Doctor
        exclude = ['user', 'is_verified', 'profile_picture_thumbnail']
        widgets = {
            'license_no': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'speciality': forms.TextInput(attrs={'class': 'form-control'}),
            'about': forms.Textarea(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'upload', 'rows': '5'}),
        }

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control floating'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control floating'}))

    fields = ['email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            user = User.objects.filter(email=email)
            if not user:
                raise forms.ValidationError("Invalid email")
        return email

    def clean_password(self):
        # passeord length must be greater than 8 characters
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long")
        return password

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError("Invalid email or password")
            if not user.is_active:
                raise forms.ValidationError("This user is not active")
        return self.cleaned_data

class RegistrationForm(forms.Form):
    
    email = forms.EmailField(label='Email', max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control floating' , 'placeholder': 'Email'}))
    phone_no = forms.CharField(label='Phone No', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control floating', 'placeholder': 'Phone No'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control floating', 'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control floating', 'placeholder': 'Confirm Password'}))

    fields = ['email', 'phone_no', 'password', 'confirm_password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('Email is required')
        return email

    def clean_phone_no(self):
        phone_no = self.cleaned_data.get('phone_no')
        if not phone_no:
            raise forms.ValidationError('Phone No is required')
        return phone_no

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError('Password is required')
        return password

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data.get('confirm_password')
        if not confirm_password:
            raise forms.ValidationError('Confirm Password is required')
        return confirm_password

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        email = cleaned_data.get('email')
        phone_no = cleaned_data.get('phone_no')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if not email or not phone_no or not password or not confirm_password:
            raise forms.ValidationError('All fields are required')
        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')
        return cleaned_data

    def save(self):
        username = self.cleaned_data.get('email')
        email = self.cleaned_data.get('email')
        phone_no = self.cleaned_data.get('phone_no')
        password = self.cleaned_data.get('password')
        # check if user already exists
        user = User.objects.filter(username=username)
        if user:
            raise forms.ValidationError('Username already exists')
        user = User.objects.filter(email=email)
        if user:
            raise forms.ValidationError('Email already exists')
        
        # pick last 9 digits of phone no
        phone_no = "254"+str(phone_no[-9:])
        user = User.objects.create_user(
            username=email,
            phone_no=phone_no, 
            email=email
            )
        user.set_password(password)
        user.is_active=False
        user.save()
        return user


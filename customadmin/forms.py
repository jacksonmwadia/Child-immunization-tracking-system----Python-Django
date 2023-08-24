from django import forms
from core.models import Vaccines
from accounts.models import Doctor
from .models import County, Hospital

class VaccineForm(forms.ModelForm):
    class Meta:
        model = Vaccines
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'time_given': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class DoctorUpdateForm(forms.ModelForm):
    class Meta:
        model = Doctor
        exclude = ['user', 'profile_picture_thumbnail']
        widgets = {
            'license_no': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'speciality': forms.TextInput(attrs={'class': 'form-control'}),
            'about': forms.Textarea(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'upload', 'rows': '5'}),
            'is_verified': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }

class HospitalForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'license_no': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'upload'}),
            'county': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control'}),
            
        }



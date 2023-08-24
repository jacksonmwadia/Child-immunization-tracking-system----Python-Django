from django import forms
from .models import Child, ChildImmunization

class ChildCreateForm(forms.ModelForm):
    class Meta:
        model = Child
        exclude = ['uuid', 'doctor']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_no': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mothers_name': forms.TextInput(attrs={'class': 'form-control'}),
            'fathers_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_registration': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'birth_county': forms.Select(attrs={'class': 'form-control'}),
            'resident_county': forms.Select(attrs={'class': 'form-control'}),
            'birth_facility': forms.TextInput(attrs={'class': 'form-control'}),
            'height': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class':'form-control select'}),
            'parent': forms.Select(attrs={'class':'form-control select'}),
        }


class ChildImmunizationForm(forms.ModelForm):
    class Meta:
        model = ChildImmunization
        exclude = ['child', 'vaccine','doctor','uuid']

        widgets = {
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'height': forms.NumberInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
            'date_given': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_vaccinated': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }
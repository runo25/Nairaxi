# apps/vehicles/forms.py
from django import forms
from .models import VehicleCategory, VehicleMake

class VehicleFilterForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=VehicleCategory.objects.all(),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2.5 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-accent focus:border-accent'
        })
    )

    make = forms.ModelChoiceField(
        queryset=VehicleMake.objects.all(),
        required=False,
        empty_label="All Makes",
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2.5 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-accent focus:border-accent'
        })
    )
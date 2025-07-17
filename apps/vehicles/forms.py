# apps/vehicles/forms.py
from django import forms
from .models import VehicleCategory, VehicleMake

class VehicleFilterForm(forms.Form):
    # Filter by Category
    category = forms.ModelChoiceField(
        queryset=VehicleCategory.objects.all(),
        required=False,
        empty_label="All Categories", # This will be the first option, e.g., "All Categories"
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2.5 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-nairaxi-blue focus:border-nairaxi-blue'
        })
    )

    # Filter by Make
    make = forms.ModelChoiceField(
        queryset=VehicleMake.objects.all(),
        required=False,
        empty_label="All Makes",
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2.5 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-nairaxi-blue focus:border-nairaxi-blue'
        })
    )

    # We can add more filters here later, like price range or ordering
    # ...
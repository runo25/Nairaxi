# apps/leasing/forms.py
from django import forms
from .models import LeaseApplication

class LeaseApplicationForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-input block w-full rounded-md border-gray-300 shadow-sm focus:border-accent focus:ring focus:ring-accent focus:ring-opacity-50',
                'type': 'date',
                'placeholder': 'Select start date'
            }
        )
    )
    end_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-input block w-full rounded-md border-gray-300 shadow-sm focus:border-accent focus:ring focus:ring-accent focus:ring-opacity-50',
                'type': 'date',
                'placeholder': 'Select end date'
            }
        )
    )
    drivers_license = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-input block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-accent/10 file:text-accent hover:file:bg-accent/20'})
    )
    identification_document = forms.FileField(
        label="Identification (e.g., NIN Slip, Passport)",
        widget=forms.FileInput(attrs={'class': 'form-input block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-accent/10 file:text-accent hover:file:bg-accent/20'})
    )
    
    terms_agreed = forms.BooleanField(
        required=True,
        label="I have read and agree to the lease terms and conditions.",
        widget=forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-accent border-gray-300 rounded focus:ring-accent'})
    )

    class Meta:
        model = LeaseApplication
        fields = ['start_date', 'end_date', 'drivers_license', 'identification_document', 'terms_agreed']
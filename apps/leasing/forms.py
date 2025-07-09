# apps/leasing/forms.py
from django import forms
from .models import LeaseApplication # We will create this model next

class LeaseApplicationForm(forms.ModelForm):
    # Using a date picker for these fields is highly recommended on the frontend.
    # We can use HTML5 date inputs initially.
    start_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-input block w-full rounded-md border-gray-300 shadow-sm focus:border-nairaxi-blue focus:ring focus:ring-nairaxi-blue focus:ring-opacity-50',
                'type': 'date', # Use browser's native date picker
                'placeholder': 'Select start date'
            }
        )
    )
    end_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-input block w-full rounded-md border-gray-300 shadow-sm focus:border-nairaxi-blue focus:ring focus:ring-nairaxi-blue focus:ring-opacity-50',
                'type': 'date',
                'placeholder': 'Select end date'
            }
        )
    )
    # Assuming you'll have fields for document uploads on the model
    drivers_license = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-input block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-nairaxi-blue hover:file:bg-blue-100'})
    )
    identification_document = forms.FileField(
        label="Identification (e.g., NIN Slip, Passport)",
        widget=forms.FileInput(attrs={'class': 'form-input block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-nairaxi-blue hover:file:bg-blue-100'})
    )
    
    terms_agreed = forms.BooleanField(
        required=True,
        label="I have read and agree to the lease terms and conditions.",
        widget=forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-nairaxi-blue border-gray-300 rounded focus:ring-nairaxi-blue'})
    )

    class Meta:
        model = LeaseApplication
        # List fields from your model that should be in the form
        fields = ['start_date', 'end_date', 'drivers_license', 'identification_document', 'terms_agreed']
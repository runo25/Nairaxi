# apps/core/forms.py
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'block w-full px-4 py-3 border-gray-300 rounded-md shadow-sm focus:ring-nairaxi-blue focus:border-nairaxi-blue',
            'placeholder': 'Your Full Name'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'block w-full px-4 py-3 border-gray-300 rounded-md shadow-sm focus:ring-nairaxi-blue focus:border-nairaxi-blue',
            'placeholder': 'your.email@example.com'
        })
    )
    subject = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'block w-full px-4 py-3 border-gray-300 rounded-md shadow-sm focus:ring-nairaxi-blue focus:border-nairaxi-blue',
            'placeholder': 'Subject of your inquiry'
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'block w-full px-4 py-3 border-gray-300 rounded-md shadow-sm focus:ring-nairaxi-blue focus:border-nairaxi-blue',
            'rows': 5,
            'placeholder': 'How can we help you today?'
        })
    )
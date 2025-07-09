# apps/accounts/forms.py
from allauth.account.forms import LoginForm, SignupForm
from django import forms

class CustomLoginForm(LoginForm):
    """
    Custom login form to apply Tailwind CSS classes.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        common_attrs = {
            'class': 'appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
        }
        
        self.fields['login'].widget.attrs.update(common_attrs)
        self.fields['login'].widget.attrs['placeholder'] = 'Email Address'
        
        self.fields['password'].widget.attrs.update(common_attrs)
        self.fields['password'].widget.attrs['placeholder'] = 'Password'


class CustomSignupForm(SignupForm):
    """
    Custom signup form to add first_name and last_name fields and apply styles.
    """
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        common_attrs = {
            'class': 'appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        }
        for field_name, field in self.fields.items():
            field.widget.attrs.update(common_attrs)
            if field.label:
                 field.widget.attrs['placeholder'] = field.label

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user
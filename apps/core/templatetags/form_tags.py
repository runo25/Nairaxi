# apps/core/templatetags/form_tags.py
from django import template

register = template.Library()

@register.simple_tag
def render_field(field, **kwargs):
    field.field.widget.attrs.update(kwargs)
    return field

@register.filter
def as_field_group(field):
    """ Renders a form field with its label and errors in a div. """
    return field.as_widget(attrs={
        'class': 'block w-full px-4 py-3 border-gray-300 rounded-md shadow-sm focus:ring-accent focus:border-accent',
        'placeholder': field.label
    })

@register.filter(name='add_class')
def add_class(field, css):
    return field.as_widget(attrs={"class": css})

@register.filter(name='add_placeholder')
def add_placeholder(field, placeholder_text):
    field.field.widget.attrs.update({'placeholder': placeholder_text or field.label})
    return field
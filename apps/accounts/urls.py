# apps/accounts/urls.py

from django.urls import path, include
from .views import dashboard_view

urlpatterns = [
    # This is your custom dashboard view.
    path('dashboard/', dashboard_view, name='account_dashboard'),
]
# apps/leasing/urls.py
from django.urls import path
from . import views

app_name = 'leasing'

urlpatterns = [
    # URL to show and submit the lease application form
    path('apply/<slug:vehicle_slug>/', views.create_lease_application, name='create_lease_application'),

    path('application-submitted/<int:application_id>/', views.application_submitted_view, name='application_submitted'),
    
    # URL for the user to view payment details and start the Paystack process
    path('pay/<int:application_id>/', views.initiate_payment, name='initiate_payment'),
    
    # URL that Paystack redirects the user back to for verification
    path('verify-payment/<str:reference>/', views.verify_payment, name='verify_payment'),
    
    # Simple static pages for redirecting after payment verification
    path('receipt/<str:reference>/', views.payment_receipt_view, name='payment_receipt'),
    path('payment/failed/', views.payment_failed, name='payment_failed'),

    # Optional but recommended: The webhook URL for server-to-server updates
    path('webhook/paystack/', views.paystack_webhook, name='paystack_webhook'),
]
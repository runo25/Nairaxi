# apps/leasing/views.py

import requests  # For making API calls to Paystack
import json      # For handling webhook data
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from apps.vehicles.models import Vehicle
from .forms import LeaseApplicationForm
from .models import LeaseApplication, Payment
from django.core.mail import send_mail # Import send_mail
from django.template.loader import render_to_string # To render email templates

# --- View 1: Create the Lease Application ---
@login_required
def create_lease_application(request, vehicle_slug):
    vehicle = get_object_or_404(Vehicle, slug=vehicle_slug, availability_status='Available')

    if request.method == 'POST':
        form = LeaseApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.customer = request.user
            application.vehicle = vehicle
            application.save() # This now also calculates and saves initial_payment_due
            
            messages.success(request, f"Your lease application for the {vehicle} has been submitted successfully! We will review it shortly.")
            # Redirect to a user dashboard or homepage after applying
            return redirect('leasing:application_submitted', application_id=application.id)
    else:
        form = LeaseApplicationForm()

    context = {
        'form': form,
        'vehicle': vehicle
    }
    return render(request, 'leasing/lease_application.html', context)


@login_required
def application_submitted_view(request, application_id):
    """
    Displays a confirmation page after a lease application is successfully submitted.
    """
    application = get_object_or_404(LeaseApplication, pk=application_id, customer=request.user)
    context = {
        'application': application,
    }
    return render(request, 'leasing/application_submitted.html', context)




# --- View 2: Show Payment Details and Paystack Button ---
@login_required
def initiate_payment(request, application_id):
    try:
        application = LeaseApplication.objects.get(pk=application_id, customer=request.user)
    except LeaseApplication.DoesNotExist:
        raise Http404("Lease application not found.")

    if application.status != 'Approved':
        messages.warning(request, "This application is not yet approved for payment.")
        return redirect('core:nairaxi_home') # Or user dashboard

    # Create or get a pending payment record.
    # This prevents creating a new payment record every time the user refreshes the page.
    payment, created = Payment.objects.get_or_create(
        lease_application=application,
        status='Pending',
        defaults={'amount': application.initial_payment_due, 'email': request.user.email}
    )
    # If the payment record existed, ensure the amount is up-to-date.
    if not created:
        payment.amount = application.initial_payment_due
        payment.email = request.user.email
        payment.save()

    context = {
        'payment': payment,
        'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY,
    }
    return render(request, 'leasing/make_payment.html', context)








# --- REVISE View 3: Verify Payment ---
@login_required
def verify_payment(request, reference):
    try:
        payment = Payment.objects.get(reference=reference, lease_application__customer=request.user)
    except Payment.DoesNotExist:
        messages.error(request, "Invalid payment reference.")
        return redirect('core:nairaxi_home')

    # If already successful, just redirect to the receipt page to prevent re-processing
    if payment.status == 'Successful':
        return redirect('leasing:payment_receipt', reference=payment.reference)

    url = f'https://api.paystack.co/transaction/verify/{reference}'
    headers = {'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        response_data = response.json()

        if response_data['status'] is True and response_data['data']['status'] == 'success':
            paystack_amount_kobo = response_data['data']['amount']
            if int(payment.amount * 100) == paystack_amount_kobo:
                payment.status = 'Successful'
                payment.paystack_charge_id = response_data['data']['id']
                # You can parse and save the paid_at timestamp from response_data['data']['paid_at']
                payment.save()

                lease = payment.lease_application
                lease.status = 'Active'
                lease.save()
                
                vehicle = lease.vehicle
                vehicle.availability_status = 'Leased'
                vehicle.save()
                
                # Instead of a simple message, we redirect to a detailed receipt page
                # The receipt page can show its own success message
                return redirect('leasing:payment_receipt', reference=payment.reference)
            else:
                payment.status = 'Failed'
                payment.save()
                messages.error(request, "Payment amount mismatch. Please contact support.")
        else:
            payment.status = 'Failed'
            payment.save()
            gateway_response = response_data.get('data', {}).get('gateway_response', 'Payment failed.')
            messages.error(request, f"Payment failed: {gateway_response}")

    except requests.exceptions.RequestException:
        messages.error(request, f"Could not connect to payment service. Please try again later.")
    
    return redirect('leasing:payment_failed') # Redirect to failure page on any error










# --- View 3: Verify Payment after User is Redirected from Paystack ---
@login_required
def verify_payment(request, reference):
    try:
        payment = Payment.objects.get(reference=reference, lease_application__customer=request.user)
    except Payment.DoesNotExist:
        messages.error(request, "Invalid payment reference.")
        return redirect('core:nairaxi_home')

    if payment.status == 'Successful':
        messages.info(request, "This payment has already been verified.")
        return redirect('leasing:payment_success') # Go to success page

    url = f'https://api.paystack.co/transaction/verify/{reference}'
    headers = {'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # Raise an exception for HTTP errors
        response_data = response.json()

        if response_data['status'] is True and response_data['data']['status'] == 'success':
            paystack_amount_kobo = response_data['data']['amount']
            if int(payment.amount * 100) == paystack_amount_kobo:
                payment.status = 'Successful'
                payment.paystack_charge_id = response_data['data']['id']
                payment.save()

                lease = payment.lease_application
                lease.status = 'Active'
                lease.save()
                
                vehicle = lease.vehicle
                vehicle.availability_status = 'Leased'
                vehicle.save()
                
                messages.success(request, f"Payment for {lease.vehicle} was successful!")
                return redirect('leasing:payment_success')
            else:
                payment.status = 'Failed'
                payment.save()
                messages.error(request, "Payment amount mismatch. Please contact support.")
        else:
            payment.status = 'Failed'
            payment.save()
            gateway_response = response_data.get('data', {}).get('gateway_response', 'Payment failed.')
            messages.error(request, f"Payment failed: {gateway_response}")

    except requests.exceptions.RequestException as e:
        messages.error(request, f"Could not connect to payment service. Please try again later.")
    
    return redirect('leasing:payment_failed') # Redirect to failure page

# --- Optional but Recommended: Webhook View ---
@csrf_exempt
def paystack_webhook(request):
    # This view is for receiving server-to-server notifications from Paystack
    # It's a more reliable way to confirm payments than just the user redirect.
    if request.method == 'POST':
        # You should verify the request is from Paystack using the signature
        # For now, we'll just process the payload.
        payload = json.loads(request.body)
        event = payload.get('event')

        if event == 'charge.success':
            data = payload.get('data')
            reference = data.get('reference')
            try:
                # Same verification logic as in verify_payment
                payment = Payment.objects.get(reference=reference)
                paystack_amount_kobo = data['amount']
                if int(payment.amount * 100) == paystack_amount_kobo and payment.status != 'Successful':
                    payment.status = 'Successful'
                    payment.save()
                    # Update lease and vehicle status...
            except Payment.DoesNotExist:
                # Log this, as it's an unexpected reference
                pass
        
        # Always return a 200 OK to Paystack to acknowledge receipt
        return HttpResponse(status=200)
    
    # Return a 400 for non-POST requests
    return HttpResponse(status=400)


# --- REVISE View 4: Rename payment_success to payment_receipt_view ---
@login_required
def payment_receipt_view(request, reference):
    """
    Displays a detailed receipt for a successful payment.
    """
    payment = get_object_or_404(Payment, reference=reference, status='Successful', lease_application__customer=request.user)
    context = {
        'payment': payment,
    }
    return render(request, 'leasing/payment_receipt.html', context)

# --- View 5: payment_failed remains the same ---
def payment_failed(request):
    return render(request, 'leasing/payment_failed.html')

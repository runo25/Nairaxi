# apps/leasing/admin.py
from .models import LeaseApplication, Payment
from django.contrib import admin, messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings
from .models import LeaseApplication, Payment

@admin.action(description="Approve selected applications and notify customers")
def approve_and_notify(modeladmin, request, queryset):
    """
    Custom admin action to approve applications and send notification emails.
    """
    approved_count = 0
    for application in queryset:
        if application.status == 'Pending':
            application.status = 'Approved'
            application.save()

            # Prepare and send email
            try:
                payment_url = request.build_absolute_uri(
                    reverse('leasing:initiate_payment', args=(application.id,))
                )
                subject = f"Your Fleet Lease Application for {application.vehicle} has been Approved!"
                message = render_to_string('leasing/emails/application_approved_user.txt', {
                    'user': application.customer,
                    'application': application,
                    'payment_url': payment_url,
                })
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[application.customer.email],
                    fail_silently=False,
                )
                approved_count += 1
            except Exception as e:
                modeladmin.message_user(
                    request,
                    f"Error sending approval email for application {application.id}: {e}",
                    messages.ERROR,
                )
    
    if approved_count > 0:
        modeladmin.message_user(
            request,
            f"{approved_count} lease application(s) were successfully approved and customers have been notified.",
            messages.SUCCESS,
        )

@admin.register(LeaseApplication)
class LeaseApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'vehicle', 'status', 'application_date', 'initial_payment_due')
    list_filter = ('status', 'application_date')
    search_fields = ('customer__username', 'customer__email', 'vehicle__vehicle_model__name')
    list_editable = ('status',) # Allows you to change the status directly from the list view!
    readonly_fields = ('application_date', 'last_updated', 'initial_payment_due')
    date_hierarchy = 'application_date'

    actions = [approve_and_notify]

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('reference', 'lease_application', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('reference', 'email', 'lease_application__customer__username')
    readonly_fields = ('reference', 'paystack_charge_id', 'paid_at', 'created_at')
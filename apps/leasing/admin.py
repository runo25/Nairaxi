# apps/leasing/admin.py
from django.contrib import admin
from .models import LeaseApplication, Payment

@admin.register(LeaseApplication)
class LeaseApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'vehicle', 'status', 'application_date', 'initial_payment_due')
    list_filter = ('status', 'application_date')
    search_fields = ('customer__username', 'customer__email', 'vehicle__vehicle_model__name')
    list_editable = ('status',) # Allows you to change the status directly from the list view!
    readonly_fields = ('application_date', 'last_updated', 'initial_payment_due')
    date_hierarchy = 'application_date'

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('reference', 'lease_application', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('reference', 'email', 'lease_application__customer__username')
    readonly_fields = ('reference', 'paystack_charge_id', 'paid_at', 'created_at')
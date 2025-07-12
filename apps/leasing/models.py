# apps/leasing/models.py
from django.db import models
from django.conf import settings # To link to the User model
from apps.vehicles.models import Vehicle
import secrets # For generating a unique reference
from decimal import Decimal


class LeaseApplication(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending Review'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Active', 'Lease Active'),
        ('Completed', 'Lease Completed'),
    ]

    # Use settings.AUTH_USER_MODEL to avoid circular imports if User model is extended
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lease_applications')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='lease_applications')
    
    start_date = models.DateField()
    end_date = models.DateField()
    
    # We need to configure MEDIA_ROOT and MEDIA_URL correctly for file uploads
    drivers_license = models.FileField(upload_to='lease_documents/licenses/%Y/%m/')
    identification_document = models.FileField(upload_to='lease_documents/ids/%Y/%m/')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    terms_agreed = models.BooleanField(default=False)
    
    application_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    initial_payment_due = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def calculate_initial_payment(self):
        # Example logic: first month's rate + security deposit
        # This should be adapted to your business logic
        deposit = self.vehicle.security_deposit_ngn or Decimal('0.00')
        # Use Decimal() for the multiplier for explicitness
        first_month = self.vehicle.monthly_rate_ngn or (self.vehicle.daily_rate_ngn * Decimal('30'))
        return deposit + first_month

    def __str__(self):
        return f"Lease Application for {self.vehicle} by {self.customer.username}"

    class Meta:
        ordering = ['-application_date']

    def save(self, *args, **kwargs):
        if not self.pk: # Only on creation
            self.initial_payment_due = self.calculate_initial_payment()
        super().save(*args, **kwargs)

class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Successful', 'Successful'),
        ('Failed', 'Failed'),
    ]
    
    lease_application = models.ForeignKey(LeaseApplication, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    email = models.EmailField()
    reference = models.CharField(max_length=200, db_index=True, unique=True, blank=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    
    paystack_charge_id = models.CharField(max_length=200, blank=True, null=True)
    paid_at = models.DateTimeField(blank=True, null=True) # Will be set by webhook
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.reference:
            # Generate a unique reference for this transaction
            while True:
                ref = secrets.token_urlsafe(20)
                if not Payment.objects.filter(reference=ref).exists():
                    self.reference = ref
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payment of {self.amount} for {self.lease_application}"
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MinValueValidator
from decimal import Decimal

# It's good practice to put choices at the module level or in a separate choices.py
# if they are used in multiple places or are extensive.
FUEL_TYPE_CHOICES = [
    ('Petrol', 'Petrol'),
    ('Diesel', 'Diesel'),
    ('Electric', 'Electric'),
    ('Hybrid', 'Hybrid'),
]

TRANSMISSION_CHOICES = [
    ('Automatic', 'Automatic'),
    ('Manual', 'Manual'),
]

class VehicleMake(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="E.g., Toyota, BMW, Mercedes-Benz")
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    # Optional: logo image

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Vehicle Make"
        verbose_name_plural = "Vehicle Makes"

class VehicleModel(models.Model):
    make = models.ForeignKey(VehicleMake, on_delete=models.CASCADE, related_name="models")
    name = models.CharField(max_length=100, help_text="E.g., Camry, X5, C-Class")
    slug = models.SlugField(max_length=120, blank=True) # Slug can be unique_together with make if needed

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.make.name}-{self.name}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.make.name} {self.name}"

    class Meta:
        ordering = ['make__name', 'name']
        unique_together = ('make', 'name') # Ensures model name is unique per make
        verbose_name = "Vehicle Model"
        verbose_name_plural = "Vehicle Models"


class VehicleCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="E.g., Sedan, SUV, Van, Shortlet Apartment, Luxury")
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    # Optional: icon

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Vehicle Category"
        verbose_name_plural = "Vehicle Categories"

class VehicleFeature(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="E.g., Air Conditioning, GPS Navigation, Sunroof, Leather Seats, Bluetooth")
    # Optional: icon, description

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Vehicle Feature"
        verbose_name_plural = "Vehicle Features"

class Vehicle(models.Model):
    AVAILABILITY_STATUS_CHOICES = [
        ('Available', 'Available for Lease'),
        ('Leased', 'Currently Leased'),
        ('Maintenance', 'Under Maintenance'),
        ('Unavailable', 'Temporarily Unavailable'),
    ]

    # Using VehicleModel which combines Make and Model name
    vehicle_model = models.ForeignKey(VehicleModel, on_delete=models.PROTECT, related_name="vehicles", help_text="Select the make and model")
    category = models.ForeignKey(VehicleCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="vehicles", help_text="E.g., Sedan, SUV, Shortlet Apartment")
    
    year = models.PositiveIntegerField(help_text="Year of manufacture, e.g., 2022")
    color = models.CharField(max_length=50, blank=True)
    license_plate = models.CharField(max_length=20, unique=True, blank=True, null=True, help_text="Vehicle registration number (optional, for tracking)")
    mileage = models.PositiveIntegerField(blank=True, null=True, help_text="Current mileage in kilometers (optional)")
    
    engine_details = models.CharField(max_length=100, blank=True, help_text="E.g., 2.5L 4-Cylinder, V6 Turbo")
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPE_CHOICES, blank=True)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES, blank=True)
    
    description = models.TextField(help_text="Detailed description of the vehicle, its condition, and unique selling points.")
    features = models.ManyToManyField(VehicleFeature, blank=True, related_name="vehicles")

    # Leasing Rates
    daily_rate_ngn = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], help_text="Price per day in NGN.")
    weekly_rate_ngn = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], blank=True, null=True, help_text="Optional: Price per week in NGN.")
    monthly_rate_ngn = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], blank=True, null=True, help_text="Optional: Price per month in NGN.")
    
    # Security deposit (can also be part of LeaseTerms model later if more complex)
    security_deposit_ngn = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Refundable security deposit in NGN.")

    main_image = models.ImageField(upload_to='vehicles/main_images/%Y/%m/', help_text="Primary image for the vehicle listing.")
    # Additional images will be handled by VehicleImage model

    availability_status = models.CharField(max_length=20, choices=AVAILABILITY_STATUS_CHOICES, default='Available')
    is_published = models.BooleanField(default=True, help_text="Visible on the website.")
    is_featured = models.BooleanField(default=False, help_text="Display on homepage featured section.")
    
    slug = models.SlugField(max_length=255, unique=True, blank=True, help_text="URL-friendly identifier, auto-generated.")
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Create a unique slug, e.g., "toyota-camry-2022-random_chars" if titles aren't unique enough
            base_slug_str = f"{self.vehicle_model.make.name}-{self.vehicle_model.name}-{self.year}"
            self.slug = slugify(base_slug_str)
            # Add logic here for ensuring slug uniqueness if multiple identical vehicles exist
            # For example, appending a short unique ID if the base slug is taken.
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # Ensure you have a URL pattern named 'vehicle_detail' in your vehicles app urls.py
        return reverse('vehicles:vehicle_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f"{self.vehicle_model} ({self.year})"

    class Meta:
        ordering = ['-date_added']
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles"

class VehicleImage(models.Model):
    vehicle = models.ForeignKey(Vehicle, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='vehicles/gallery/%Y/%m/%d/')
    caption = models.CharField(max_length=150, blank=True, help_text="Optional caption for the image.")
    is_primary_gallery = models.BooleanField(default=False, help_text="If true, this could be used as the default image if Vehicle.main_image isn't set, or for ordering.")
    # order = models.PositiveIntegerField(default=0, blank=False, null=False) # For custom ordering of gallery images

    def __str__(self):
        return f"Image for {self.vehicle}"

    class Meta:
        ordering = ['vehicle', '-is_primary_gallery'] # Order by primary then by default
        verbose_name = "Vehicle Image"
        verbose_name_plural = "Vehicle Images"
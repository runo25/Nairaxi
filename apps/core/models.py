from django.db import models

# Create your models here.
# apps/core/models.py
from django.db import models
from django.core.exceptions import ValidationError

class SiteSettings(models.Model):
    # This is a Singleton model - we only want one instance of it.
    
    # --- Contact Information ---
    primary_phone_number = models.CharField(max_length=20, blank=True, help_text="e.g., +234 915 5541 159")
    secondary_phone_number = models.CharField(max_length=20, blank=True, help_text="Optional second contact number")
    primary_whatsapp_number = models.CharField(max_length=20, blank=True, help_text="WhatsApp number including country code, e.g., 2349155541159 (no '+')")
    primary_email = models.EmailField(blank=True, help_text="Main contact/support email address")
    office_address = models.TextField(blank=True, help_text="Full office address, use line breaks for formatting.")

    # --- Social Media Links ---
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True, help_text="URL for your X (formerly Twitter) profile")
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    
    # --- Dynamic Colors ---
    # We define fallback default colors that match our initial Tailwind config
    color_brand_primary = models.CharField(max_length=7, default='#1993e5', help_text="Primary brand color (e.g., buttons, accents)")
    color_brand_secondary = models.CharField(max_length=7, default='#111518', help_text="Secondary color (e.g., dark text, headings)")
    # Add more color fields as needed, e.g., color_accent, color_background, etc.

    # --- Legal & Footer ---
    footer_copyright_text = models.CharField(max_length=200, blank=True, default="Fleet Car Leasing. All rights reserved.")

    def __str__(self):
        return "Site Configuration"

    def clean(self):
        # Enforce that only one instance of SiteSettings can be created.
        if SiteSettings.objects.exists() and not self.pk:
            raise ValidationError("There can be only one SiteSettings instance. Please edit the existing one.")

    def save(self, *args, **kwargs):
        self.pk = 1 # Set the primary key to 1 to ensure it's a singleton
        super(SiteSettings, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Prevent deletion of the singleton instance
        pass

    class Meta:
        verbose_name_plural = "Site Configuration"

# We might also have a model for Testimonials here if we haven't created it yet
# class Testimonial(models.Model):
#     ...
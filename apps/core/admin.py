# apps/core/admin.py
from django.contrib import admin
from .models import SiteSettings #, Testimonial

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('__str__',) # Only one item, so not much to list
    
    # This prevents users from adding new SiteSettings instances from the admin
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

# admin.site.register(Testimonial)
# apps/core/context_processors.py
from .models import SiteSettings

def site_settings_context(request):
    """
    Makes the SiteSettings object available in all templates as 'site_settings'.
    """
    try:
        settings = SiteSettings.objects.get(pk=1)
    except SiteSettings.DoesNotExist:
        # Create a default instance if none exists
        settings = SiteSettings.objects.create(pk=1) 
    
    return {'site_settings': settings}
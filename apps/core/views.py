from apps.vehicles.models import Vehicle # Import the Vehicle model
# from .models import SiteSettings, Testimonial # Assuming these are still needed or handled by context processor
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import ContactForm # We will create/confirm this form
from django.http import HttpResponse
from .models import SiteSettings


def dynamic_colors_css(request):
    try:
        settings = SiteSettings.objects.get(pk=1)
    except SiteSettings.DoesNotExist:
        settings = SiteSettings() # Use default values if no instance exists

    css_template = """
    :root {{
        --color-brand-primary: {primary};
        --color-brand-secondary: {secondary};
        /* Add more CSS variables for other dynamic colors here */
    }}
    """
    css = css_template.format(
        primary=settings.color_brand_primary,
        secondary=settings.color_brand_secondary,
    )
    return HttpResponse(css, content_type='text/css')


def nairaxi_home_page(request):
    # Fetch featured vehicles: published and marked as featured, limit to 3-4, newest first
    featured_vehicles = Vehicle.objects.filter(
        is_published=True, 
        is_featured=True
    ).order_by('-date_added')[:3] # Get the latest 3 featured vehicles

    # Fetch testimonials if you have that model and want them on homepage
    # testimonials = Testimonial.objects.filter(is_approved=True).order_by('-date_received')[:2]
    
    # SiteSettings is likely handled by a context processor, if not, fetch it here:
    # site_settings = SiteSettings.objects.first()

    context = {
        'featured_vehicles': featured_vehicles,
        # 'testimonials': testimonials,
        # 'site_settings': site_settings, # Only if not using context processor
    }

    return render(request, 'core/nairaxi_index.html', context)
def car_viewer_view(request):
    return render(request, 'core/car_viewer.html') # Ensure template path is correct


def faq_page(request):
    # In the future, you could fetch FAQ items from a model in the database.
    # For now, the content will be directly in the template.
    context = {}
    return render(request, 'core/faq.html', context)

def about_us_page(request):
    return render(request, 'core/about_us.html') # Ensure template path is correct


def contact_us_page(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            from_email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message_body = form.cleaned_data['message']

            email_subject = f"Website Contact Form: {subject}"
            email_message = f"You have a new message from {name} ({from_email}).\n\nMessage:\n{message_body}"
            
            try:
                send_mail(
                    email_subject,
                    email_message,
                    settings.DEFAULT_FROM_EMAIL, # Or a no-reply address
                    [settings.PRIMARY_CONTACT_EMAIL] # Your company's support email
                )
                messages.success(request, 'Your message has been sent successfully! We will get back to you shortly.')
                return redirect('core:contact_us')
            except Exception as e:
                messages.error(request, 'Sorry, there was an error sending your message. Please try again or contact us directly.')
    else:
        form = ContactForm()

    # The site_settings context processor should make `site_settings` globally available
    context = {
        'form': form,
    }
    return render(request, 'core/contact.html', context)
# apps/vehicles/views.py
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Vehicle # Assuming you'll list Vehicle objects
# from .forms import PropertyFilterForm # If you have a filter form
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def vehicle_list_view(request):
    # Basic placeholder logic - we'll enhance this later
    vehicle_list_qs = Vehicle.objects.filter(is_published=True).order_by('-date_added')
    
    # Example of adding filter form logic if you have it
    # filter_form = PropertyFilterForm(request.GET or None)
    # if filter_form.is_valid():
    #     # Apply filters to vehicle_list_qs
    #     pass

    # Search functionality
    keywords = request.GET.get('keywords', '')
    if keywords:
        vehicle_list_qs = vehicle_list_qs.filter(
            Q(vehicle_model__name__icontains=keywords) |
            Q(description__icontains=keywords) |
            Q(vehicle_model__make__name__icontains=keywords)
        ).distinct()

    paginator = Paginator(vehicle_list_qs, 9) # Show 9 vehicles per page
    page_number = request.GET.get('page')
    try:
        vehicles = paginator.page(page_number)
    except PageNotAnInteger:
        vehicles = paginator.page(1)
    except EmptyPage:
        vehicles = paginator.page(paginator.num_pages)

    context = {
        'vehicles': vehicles,
        # 'filter_form': filter_form,
    }
    # You will need to create this template: apps/vehicles/templates/vehicles/vehicle_list.html
    return render(request, 'vehicles/vehicle_list.html', context)





def vehicle_detail_view(request, slug):
    # Fetch the main vehicle object, or return a 404 error if not found
    vehicle = get_object_or_404(Vehicle, slug=slug, is_published=True)

    # --- LOGIC FOR RELATED VEHICLES ---
    related_vehicles = Vehicle.objects.filter(
        # Find vehicles that are in the same category OR from the same make
        Q(category=vehicle.category) | Q(vehicle_model__make=vehicle.vehicle_model.make),
        is_published=True
    ).exclude(
        # Exclude the current vehicle itself from the list
        pk=vehicle.pk
    ).order_by(
        '?' # Order randomly to show different suggestions each time
    )[:3] # Limit to 3 related vehicles

    # A fallback if the first query returns less than 3 vehicles
    if related_vehicles.count() < 3:
        # Get some other random published vehicles to fill the remaining spots
        additional_vehicles = Vehicle.objects.filter(
            is_published=True
        ).exclude(
            pk=vehicle.pk
        ).exclude(
            # Exclude vehicles we already have
            pk__in=[v.pk for v in related_vehicles]
        ).order_by('?')[:3 - related_vehicles.count()]
        
        # Combine the querysets
        # Note: In Django < 4.0, combining querysets with '|' after slicing/ordering can be tricky.
        # This approach is safer across versions.
        related_vehicles = list(related_vehicles) + list(additional_vehicles)


    # Combine main_image and gallery images into one list for the main gallery
    gallery_images = []
    if vehicle.main_image:
        gallery_images.append(vehicle.main_image)
    
    other_images = vehicle.images.all()
    if vehicle.main_image:
        # Exclude the main image from the gallery queryset if it's already added
        other_images = other_images.exclude(image__exact=vehicle.main_image.name)
        
    for img in other_images:
        gallery_images.append(img.image)

    context = {
        'vehicle': vehicle,
        'gallery_images': gallery_images,
        'related_vehicles': related_vehicles, # <-- Add this to the context
    }
    return render(request, 'vehicles/vehicle_detail.html', context)
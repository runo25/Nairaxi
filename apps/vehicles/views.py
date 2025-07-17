# apps/vehicles/views.py
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Vehicle, VehicleCategory, VehicleMake # Import new models
from .forms import VehicleFilterForm # Import our new form
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def vehicle_list_view(request):
    vehicle_list_qs = Vehicle.objects.filter(is_published=True).order_by('-date_added')
    
    # Initialize form with any GET data from the URL
    filter_form = VehicleFilterForm(request.GET or None)

    if filter_form.is_valid():
        # Get cleaned data from the form
        category = filter_form.cleaned_data.get('category')
        make = filter_form.cleaned_data.get('make')
        keywords = filter_form.cleaned_data.get('keywords', request.GET.get('keywords', '')) # Keep existing keyword logic

        # Apply filters to the queryset
        if category:
            vehicle_list_qs = vehicle_list_qs.filter(category=category)
        if make:
            vehicle_list_qs = vehicle_list_qs.filter(vehicle_model__make=make)
        if keywords:
            vehicle_list_qs = vehicle_list_qs.filter(
                Q(vehicle_model__name__icontains=keywords) |
                Q(description__icontains=keywords) |
                Q(vehicle_model__make__name__icontains=keywords)
            ).distinct()

    # Pagination logic (remains the same)
    paginator = Paginator(vehicle_list_qs, 9)
    page_number = request.GET.get('page')
    try:
        vehicles = paginator.page(page_number)
    except PageNotAnInteger:
        vehicles = paginator.page(1)
    except EmptyPage:
        vehicles = paginator.page(paginator.num_pages)

    # Preserve filter parameters in pagination links
    get_params = request.GET.copy()
    if 'page' in get_params:
        del get_params['page']

    context = {
        'vehicles': vehicles,
        'filter_form': filter_form, # Pass the form to the template
        'get_params_urlencode': get_params.urlencode(),
    }
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
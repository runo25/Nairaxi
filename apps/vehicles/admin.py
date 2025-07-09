from django.contrib import admin
from .models import VehicleMake, VehicleModel, VehicleCategory, VehicleFeature, Vehicle, VehicleImage

class VehicleImageInline(admin.TabularInline): # Or StackedInline
    model = VehicleImage
    extra = 1 # How many empty forms to show

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'vehicle_model', 'category', 'year', 'daily_rate_ngn', 'availability_status', 'is_published', 'is_featured')
    list_filter = ('availability_status', 'category', 'vehicle_model__make', 'year', 'is_published', 'is_featured')
    search_fields = ('vehicle_model__name', 'vehicle_model__make__name', 'year', 'license_plate', 'description')
    prepopulated_fields = {'slug': ('vehicle_model', 'year')} # Requires some JS or custom logic if vehicle_model is FK
    inlines = [VehicleImageInline]
    fieldsets = (
        (None, {
            'fields': ('vehicle_model', 'category', 'year', 'slug')
        }),
        ('Details', {
            'fields': ('color', 'license_plate', 'mileage', 'engine_details', 'fuel_type', 'transmission', 'description')
        }),
        ('Leasing & Pricing', {
            'fields': ('daily_rate_ngn', 'weekly_rate_ngn', 'monthly_rate_ngn', 'security_deposit_ngn')
        }),
        ('Images & Features', {
            'fields': ('main_image', 'features')
        }),
        ('Status & Visibility', {
            'fields': ('availability_status', 'is_published', 'is_featured')
        }),
    )

@admin.register(VehicleMake)
class VehicleMakeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')

@admin.register(VehicleModel)
class VehicleModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)} # Might need custom slug logic if name alone isn't unique
    list_display = ('name', 'make', 'slug')
    list_filter = ('make',)

@admin.register(VehicleCategory)
class VehicleCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')

admin.site.register(VehicleFeature)
# admin.site.register(VehicleImage) # Not needed if only used as inline
from django.urls import path
from . import views

app_name = 'vehicles'  # THIS LINE IS CRUCIAL for the 'vehicles' namespace

urlpatterns = [
    # Example: assuming you have a vehicle_list_view defined
    path('', views.vehicle_list_view, name='vehicle_list'),
    path('<slug:slug>/', views.vehicle_detail_view, name='vehicle_detail'),
    # Add other vehicle-related URLs here
]
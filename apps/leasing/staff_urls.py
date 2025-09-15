# apps/leasing/staff_urls.py
from django.urls import path
from . import views

app_name = 'leasing_staff'

urlpatterns = [
    path('', views.staff_lease_list, name='staff_lease_list'),
    path('<int:application_id>/', views.staff_lease_detail, name='staff_lease_detail'),
    path('update-status/<int:application_id>/<str:status>/', views.staff_update_lease_status, name='staff_update_lease_status'),
]

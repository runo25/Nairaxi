from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.nairaxi_home_page, name='nairaxi_home'), # New name for clarity
    path('car-viewer/', views.car_viewer_view, name='car_viewer'),
    path('faq/', views.faq_page, name='faq'), 
    path('about-us/', views.about_us_page, name='about_us'),
    path('contact-us/', views.contact_us_page, name='contact_us'),
    path('dynamic-colors.css', views.dynamic_colors_css, name='dynamic_colors_css'),
]
    # Add other core URLs later

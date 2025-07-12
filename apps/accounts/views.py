from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.leasing.models import LeaseApplication # Import the model

@login_required
def dashboard_view(request):
    # Get all lease applications for the currently logged-in user
    user_applications = LeaseApplication.objects.filter(customer=request.user).order_by('-application_date')
    
    context = {
        'applications': user_applications,
    }
    return render(request, 'accounts/dashboard.html', context)
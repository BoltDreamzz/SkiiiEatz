from django.urls import path
from . import views

app_name = 'sass'

urlpatterns = [
    path('vendor/signup/', views.vendor_signup, name='vendor_signup'),
    path('vendor/pending/', views.vendor_pending, name='vendor_pending'),
    path('vendor/dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('vendor/payout-request/', views.create_payout_request, name='create_payout_request'),
]

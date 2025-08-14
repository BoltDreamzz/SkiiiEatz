from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .forms import VendorSignupForm, PayoutRequestForm
from .models import Vendor, Business
from .decorators import vendor_required

@login_required
def vendor_signup(request):
    if hasattr(request.user, 'vendor_profile'):
        return redirect('sass:vendor_dashboard')
    if request.method == 'POST':
        form = VendorSignupForm(request.POST)
        if form.is_valid():
            vendor = form.save(commit=False)
            vendor.user = request.user
            vendor.is_approved = False
            vendor.save()
            btype = form.cleaned_data['business_type']
            Business.objects.create(vendor=vendor, business_type=btype)
            messages.success(request, "🥳 Application submitted. Wait for admin approval.")
            return redirect('sass:vendor_pending')
        else:
            messages.error(request, "❌ There was a problem with your application.")
    else:
        form = VendorSignupForm()
    return render(request, 'sass/vendor_signup.html', {'form': form})

@login_required
def vendor_pending(request):
    return render(request, 'sass/vendor_pending.html')

@login_required
@vendor_required
def vendor_dashboard(request):
    vendor = request.user.vendor_profile
    total_earnings = vendor.earnings.aggregate(Sum('net_amount'))['net_amount__sum'] or 0
    paid = vendor.earnings.filter(is_paid_out=True).aggregate(Sum('net_amount'))['net_amount__sum'] or 0
    pending = vendor.earnings.filter(is_paid_out=False).aggregate(Sum('net_amount'))['net_amount__sum'] or 0
    payouts = vendor.payout_requests.all().order_by('-requested_at')
    return render(request, 'sass/dashboard/index.html', {
        'vendor': vendor,
        'total_earnings': total_earnings,
        'paid': paid,
        'pending': pending,
        'payouts': payouts,
    })

@login_required
@vendor_required
def create_payout_request(request):
    vendor = request.user.vendor_profile
    if request.method == 'POST':
        form = PayoutRequestForm(request.POST)
        if form.is_valid():
            pr = form.save(commit=False)
            pr.vendor = vendor
            balance = vendor.earnings.filter(is_paid_out=False).aggregate(Sum('net_amount'))['net_amount__sum'] or 0
            if pr.amount > balance:
                messages.error(request, "😢 Insufficient balance for that payout.")
                return redirect('sass:vendor_dashboard')
            pr.save()
            messages.success(request, " 🥳 Payout request submitted.")
            return redirect('sass:vendor_dashboard')
    else:
        form = PayoutRequestForm()
    return render(request, 'sass/payout_request.html', {'form': form})

from django.shortcuts import redirect
from functools import wraps

def vendor_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not hasattr(request.user, 'vendor_profile'):
            return redirect('sass:vendor_signup')
        if not request.user.vendor_profile.is_approved:
            from django.contrib import messages
            messages.info(request, "Your vendor application is pending approval.")
            return redirect('sass:vendor_pending')
        return view_func(request, *args, **kwargs)
    return _wrapped

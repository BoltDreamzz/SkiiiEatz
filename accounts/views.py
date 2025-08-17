# from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import AvatarSelectionForm
from django.contrib import messages
from core.models import Order

@login_required
def change_avatar(request):
    avatars = Avatar.objects.all()
    # Get the user's profile or create one if it doesn't exist
    # If the user has no profile, redirect to create profile view

    # profile = request.user.userprofile
    profile = get_object_or_404(UserProfile, user=request.user)
    # If the user has no profile, redirect to create profile view
    if not profile:
        messages.error(request, '😢 You have no profile yet! Please create one.')
        return redirect('accounts:create_profile')

    if request.method == 'POST':
        form = AvatarSelectionForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, '😍 Avatar updated!')
            return redirect('accounts:profile')  # your profile page view name
    else:
        form = AvatarSelectionForm(instance=profile)
    return render(request, 'accounts/change_avatar.html', {'form': form, 'avatars': avatars, 'profile': profile})

from .models import UserProfile, Avatar

@login_required
def profile(request):
    avatars = Avatar.objects.all()
    orders = Order.objects.filter(user=request.user, status='completed')
    count_orders = orders.count()
    try:

        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = None
        messages.success(request, '😉 You have no profile yet!')
        return redirect('accounts:create_profile_view')
        
    return render(request, 'accounts/profile.html', {'profile': profile, 'avatars': avatars, 'orders': orders, 'count_orders': count_orders})





import random
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Avatar, UserProfile
from .forms import UserRegistrationForm, LoginForm
from .utils import generate_username
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = generate_username()  # Assign random username
            user.set_password(form.cleaned_data['password'])  # ✅ Hash password
            user.save()

            messages.success(request, '🥳 Account created. Please log in.')
            return redirect('accounts:login')
        else:
            messages.error(request, '🚫 Ooops!. please check again.')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    try:
        
        if request.method == 'POST':
            form = LoginForm(request, data=request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('username')  # In your form, username field is actually email
                password = form.cleaned_data.get('password')

                # Authenticate using custom backend
                user = authenticate(request, username=email, password=password)

                if user is not None:
                    login(request, user)

                    # Handle "keep me signed in"
                    if 'remember_me' in request.POST:
                        request.session.set_expiry(1209600)  # 2 weeks
                    else:
                        request.session.set_expiry(0)  # expires on browser close

                    messages.success(request, f'👋 Welcome back, {user.full_name}!')
                    return redirect('core:explore')  # Change to your dashboard/home URL
                else:
                    messages.error(request, '🚫 Invalid email or password.')
            else:
                messages.error(request, '🚫 Please correct the errors below.')
        else:
            form = LoginForm()
    except Exception as e:
        messages.error(request, f'Ooops! {e}')

    return render(request, 'accounts/login.html', {'form': form})

@login_required
def create_profile_view(request):
    if hasattr(request.user, 'userprofile'):
        messages.info(request, '👍 You already have a profile.')
        return redirect('accounts:profile')  # Change to your homepage

    avatars = Avatar.objects.all()
    if request.method == 'POST':
        avatar_id = request.POST.get('avatar')
        avatar = Avatar.objects.filter(id=avatar_id).first()
        UserProfile.objects.create(user=request.user, avatar=avatar)
        messages.success(request, '🥳 Profile created.')
        return redirect('accounts:profile')
    return render(request, 'accounts/create_profile.html', {'avatars': avatars})

@login_required
def change_avatar_htmx(request, avatar_id):
    profile = request.user.userprofile
    avatar = get_object_or_404(Avatar, id=avatar_id)

    profile.avatar = avatar
    profile.save()

    messages.success(request, '😍 Avatar updated!')

    # Return updated current avatar HTML only
    return render(request, 'accounts/partials/current_avatar.html', {'profile': profile})
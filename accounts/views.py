# from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import AvatarSelectionForm
from django.contrib import messages

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
    try:

        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = None
        messages.success(request, '😉 You have no profile yet!')
        
    return render(request, 'accounts/profile.html', {'profile': profile, 'avatars': avatars})





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
            user.save()

            
            messages.success(request, '🥳 Account created. Please log in.')
            return redirect('accounts:login')
        else:
            messages.error(request, '🚫 Ooops!. please check again.')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


class CustomLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'accounts/login.html'


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
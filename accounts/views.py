# from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import AvatarSelectionForm

@login_required
def change_avatar(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = AvatarSelectionForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # your profile page view name
    else:
        form = AvatarSelectionForm(instance=profile)
    return render(request, 'accounts/change_avatar.html', {'form': form})

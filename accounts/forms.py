from django import forms
from .models import UserProfile, Avatar

class AvatarSelectionForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']
        widgets = {
            'avatar': forms.RadioSelect()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar'].queryset = Avatar.objects.all()


from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User

class UserRegistrationForm(forms.ModelForm):
    email = forms.CharField(
        widget=forms.EmailInput(attrs={
            "placeholder": "eg. 'John@gmail.com'",
            "class": "input input-bordered px-6 py-6 rounded-2xl w-full bgtt-orange border border-2 border-orange-400",
        })
    )

    full_name = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "eg. John Thomas",
            "class": "input input-bordered px-6 py-6 rounded-2xl w-full bgtt-orange border border-2 border-orange-400"
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Enter a strong password",
            "class": "input input-bordered px-6 py-6 rounded-2xl w-full bgtt-orange border border-2 border-orange-400"
        })
    )

    class Meta:
        model = User
        fields = ['email', 'full_name', 'password']


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.EmailInput(attrs={
            "placeholder": "Enter your email",
            "class": "input input-bordered border border-2 w-full rounded-2xl px-6 py-6 bgtt-orange border-orange-400"
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Enter your password",
            "class": "input input-bordered px-6 py-6 w-full rounded-2xl border border-2 bgtt-orange border-orange-400"
        })
    )

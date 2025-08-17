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

# class UserRegistrationForm(forms.ModelForm):
#     email = forms.CharField(
#         widget=forms.EmailInput(attrs={
#             "placeholder": "eg. 'John@gmail.com'",
#             "class": "input input-bordered px-6 py-6 rounded-2xl w-full bgtt-orange border border-2 border-orange-400",
#         })
#     )

#     full_name = forms.CharField(
#         widget=forms.TextInput(attrs={
#             "placeholder": "eg. John Thomas",
#             "class": "input input-bordered px-6 py-6 rounded-2xl w-full bgtt-orange border border-2 border-orange-400"
#         })
#     )

#     password = forms.CharField(
#         widget=forms.PasswordInput(attrs={
#             "placeholder": "Enter a strong password",
#             "class": "input input-bordered px-6 py-6 rounded-2xl w-full bgtt-orange border border-2 border-orange-400"
#         })
#     )

#     class Meta:
#         model = User
#         fields = ['email', 'full_name', 'password']


# class LoginForm(AuthenticationForm):
#     username = forms.CharField(
#         widget=forms.EmailInput(attrs={
#             "placeholder": "Enter your email",
#             "class": "input input-bordered border border-2 w-full rounded-2xl px-6 py-6 bgtt-orange border-orange-400"
#         })
#     )
#     password = forms.CharField(
#         widget=forms.PasswordInput(attrs={
#             "placeholder": "Enter your password",
#             "class": "input input-bordered px-6 py-6 w-full rounded-2xl border border-2 bgtt-orange border-orange-400"
#         })
#     )


from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from .models import User


class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "placeholder": "eg. 'John@gmail.com'",
            "class": "input input-bordered px-6 py-6 rounded-2xl w-full bgtt-orange border border-2 border-orange-400",
            "id": "id_email"
        })
    )

    full_name = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "eg. John Thomas",
            "class": "input input-bordered px-6 py-6 rounded-2xl w-full bgtt-orange border border-2 border-orange-400",
            "id": "id_full_name"
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Enter a strong password",
            "class": "input input-bordered px-6 py-6 rounded-2xl w-full bgtt-orange border border-2 border-orange-400",
            "id": "id_password"
        })
    )

    class Meta:
        model = User
        fields = ['email', 'full_name', 'password']

    # 🔹 Email must be unique
    def clean_email(self):
        email = self.cleaned_data.get("email").lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    # 🔹 Validate full name
    def clean_full_name(self):
        full_name = self.cleaned_data.get("full_name")
        if len(full_name) < 2:
            raise ValidationError("Full name must be at least 2 characters long.")
        return full_name

    # 🔹 Password strength validation
    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in password):
            raise ValidationError("Password must contain at least one number.")
        if not any(char.isalpha() for char in password):
            raise ValidationError("Password must contain at least one letter.")
        return password


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "placeholder": "Enter your email",
            "class": "input input-bordered border border-2 w-full rounded-2xl px-6 py-6 bgtt-orange border-orange-400",
            "id": "id_username"
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Enter your password",
            "class": "input input-bordered px-6 py-6 w-full rounded-2xl border border-2 bgtt-orange border-orange-400",
            "id": "id_password"
        })
    )

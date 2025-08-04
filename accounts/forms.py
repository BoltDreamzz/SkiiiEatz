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

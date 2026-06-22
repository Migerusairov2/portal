from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['description']
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 5,
                'class': 'form-control'
            })
        }
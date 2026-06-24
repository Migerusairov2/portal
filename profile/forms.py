from django import forms
from .models import Profile, SocialMedia


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile', 'description', 'github_token']
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 5,
                'class': 'text-area',
                'placeholder': 'Fullstack Python developer...'
            }),
            'profile': forms.FileInput(attrs={
                'class': 'profile-input'
            }),
            'github_token': forms.TextInput(attrs={
                'class': 'text-input',
                'placeholder': 'github_pat_xxxxxxxxxxxx'
            })
        }



class SocialMediaForm(forms.ModelForm):

    class Meta:
        model = SocialMedia
        fields = ['name', 'url', 'logo']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Platform name'
            }),

            'url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/username'
            }),

            'logo': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }
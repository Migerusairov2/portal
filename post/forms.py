from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["caption"]
        widgets = {
            'caption': forms.Textarea(attrs={
                'placeholder': "What's on your mind?",
                'rows': 3,
            }),
        }
        labels = {
            'caption': '',
        }

    def clean(self):
        cleaned_data = super().clean()

        return cleaned_data
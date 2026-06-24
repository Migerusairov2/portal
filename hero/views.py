from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User 
from profile.models import Profile, SocialMedia

def hero(request):
    return render(request, 'hero.html')
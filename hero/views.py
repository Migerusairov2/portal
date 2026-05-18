from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User 
from adminprofile.models import Profile, SocialMedia

def hero(request):

    superuser = User.objects.filter(is_superuser=True).first()
    profile, created = Profile.objects.get_or_create(user=superuser)
    social_media = SocialMedia.objects.filter(user=superuser)

    if not superuser:
        text = "There's no Superuser created yet."
        return HttpResponse(text)
    
    context= {
        'avatar': profile.profile.url if profile.profile else False,
        'admin': superuser,
        'description': profile.description,
        'social': social_media
    }
    
    return render(request, 'hero.html', context)
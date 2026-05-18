from django.shortcuts import render
from django.contrib.auth.models import User 
from .models import Profile, Project, Trajectory, SocialMedia, GithubRepository, GithubCommit
from django.db.models import Prefetch
from django.core.management import call_command

def admin_profile(request):

    superuser = User.objects.filter(is_superuser=True).first()
    profile, created = Profile.objects.get_or_create(user=superuser)
    frameworks = profile.frameworks.all()
    languages = profile.languages.all()
    projects = Project.objects.filter(user=superuser).prefetch_related('languages_used', 'images')
    trajectories = Trajectory.objects.filter(user=superuser)
    social_medias = SocialMedia.objects.filter(user=superuser)
    # query = request.GET.get('q')

    if request.GET.get('sync') == 'github':
        call_command('fetch_github_repos')

    repos = GithubRepository.objects.all().order_by('-stars')
    repos_by_date = GithubRepository.objects.prefetch_related(
        Prefetch(
            "commits",
            queryset=GithubCommit.objects.order_by("-date")
        )
    )
    # if query:
    #     repos = repos.filter(name__icontains=query)

    # commits = GithubCommit.objects.select_related("repository")[:20]


    context = {
        'admin_profile': superuser,
        'description': profile.description,
        'avatar': profile.profile.url if profile.profile else False,
        'frameworks': frameworks,  
        'languages': languages,  
        'projects': projects,
        'trajectories': trajectories,
        'social_medias': social_medias,
        'repos': repos,
        'repos_by_date': repos_by_date
    }

    return render(request, 'admin_profile.html', context)
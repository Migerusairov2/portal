from django.http import HttpResponse
from django.contrib.auth.models import User 
from .models import Profile, Project, Trajectory, SocialMedia, GithubRepository, GithubCommit
from django.db.models import Prefetch
from django.core.management import call_command
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse



def profile(request):

    if request.user.is_authenticated:
        user = request.user
    else:
        user = User.objects.filter(is_superuser=True).first()

        if not user:
            return HttpResponse("No superuser found.")

    profile, created = Profile.objects.get_or_create(user=user)
    frameworks = profile.frameworks.all()
    languages = profile.languages.all()
    projects = Project.objects.filter(user=user).prefetch_related('languages_used', 'images')
    trajectories = Trajectory.objects.filter(user=user)
    social_medias = SocialMedia.objects.filter(user=user)

    
    # fetch superuser github only
    # if request.GET.get('sync') == 'github':
    #     call_command('fetch_github_repos')

    #     return redirect('/profile/?tab=repositories')
    

    repos = GithubRepository.objects.filter(user=user).order_by('-stars')
    print('repos', repos)
    repos_by_date = GithubRepository.objects.filter(user=user).order_by("-pushed_at").prefetch_related(
        Prefetch(
            "commits",
            queryset=GithubCommit.objects.order_by("-date")
        )
    )

    # query = request.GET.get('q')
    # if query:
    #     repos = repos.filter(name__icontains=query)

    # commits = GithubCommit.objects.select_related("repository")[:20]


    context = {
        'profile': user,
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

    return render(request, 'profile.html', context)


from .forms import ProfileForm

def edit_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {
        'form': form
    })


@login_required
def sync_github(request):

    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    if profile.github_token:
        print('True')
        call_command(
            'fetch_github_repos',
            user_id=request.user.id
        )

        return JsonResponse({"success": True})
    else:
        print('False')
        return JsonResponse({"success": False})

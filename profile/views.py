from django.http import HttpResponse
from django.contrib.auth.models import User 
from .models import Profile, Project, Trajectory, SocialMedia, GithubRepository, GithubCommit, Framework, Language, ProjectImage
from django.db.models import Prefetch
from django.core.management import call_command
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import ProfileForm, SocialMediaForm


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
    

def edit_profile(request):
    user = request.user
    profile = user.profile

    social_medias = SocialMedia.objects.filter(user=user)
    trajectories = Trajectory.objects.filter(user=user)


    frameworks = profile.frameworks.all()
    available_frameworks = Framework.objects.exclude(
        id__in=frameworks.values_list('id', flat=True)
    )

    languages = profile.languages.all()
    available_languages = Language.objects.exclude(
        id__in=languages.values_list('id', flat=True)
    )

    projects = Project.objects.filter(user=user).prefetch_related('languages_used')

    social_form = SocialMediaForm()

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {
        'form': form,
        'profile': profile,
        'social_medias': social_medias,
        'trajectories': trajectories,
        'social_form': social_form,
        'frameworks': frameworks,
        'available_frameworks': available_frameworks,
        'languages': languages,
        'available_languages': available_languages,
        'projects': projects,
        'is_edit': True,
    })

def add_social_media(request):

    if request.method == "POST":

        form = SocialMediaForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            social = form.save(commit=False)

            social.user = request.user

            social.save()

            return redirect('edit_profile')

    return redirect('edit_profile')
    

def delete_social_media(request, id):

    media = get_object_or_404(
        SocialMedia,
        id=id,
        user=request.user
    )
    media.delete()

    return redirect('edit_profile')


def remove_framework(request, id):
    framework = get_object_or_404(Framework, id=id)

    profile = request.user.profile
    profile.frameworks.remove(framework)

    return redirect("edit_profile")

@login_required
def add_framework(request):
    if request.method == "POST":
        framework = get_object_or_404(
            Framework,
            id=request.POST.get("framework_id")
        )

        request.user.profile.frameworks.add(framework)

    return redirect('edit_profile')

def remove_language(request, language_id):
    language = get_object_or_404(Language, id=language_id)
    request.user.profile.languages.remove(language)
    return redirect("edit_profile")

def add_language(request):
    if request.method == "POST":
        language_ids = request.POST.getlist("language_ids")
        languages = Language.objects.filter(id__in=language_ids)
        request.user.profile.languages.add(*languages)

    return redirect("edit_profile")



def add_project(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        url = request.POST.get("url")

        pinned = request.POST.get("pinned") == "on"

        project = Project.objects.create(
            user=request.user,
            name=name,
            description=description,
            url=url,
            pinned=pinned
        )

        language_ids = request.POST.getlist("languages")
        if language_ids:
            project.languages_used.set(language_ids)

        images = request.FILES.getlist("images")
        for index, image_file in enumerate(images):
            caption = request.POST.get(f"caption_{index}", "")
            ProjectImage.objects.create(
                project=project,
                image=image_file,
                caption=caption,
            )

    return redirect("edit_profile")

def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    if request.method == "POST":
        project.name = request.POST.get("name")
        project.description = request.POST.get("description")
        project.url = request.POST.get("url")
        project.pinned = request.POST.get("pinned") == "on"
        project.languages_used.set(request.POST.getlist("languages"))
        project.save()

        delete_ids = request.POST.getlist("delete_image")
        if delete_ids:
            project.images.filter(id__in=delete_ids).delete()

        for index, image_file in enumerate(request.FILES.getlist("images")):
            caption = request.POST.get(f"caption_{index}", "")
            ProjectImage.objects.create(project=project, image=image_file, caption=caption)

    return redirect("edit_profile")

def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.delete()
    return redirect('edit_profile')

def add_trajectory(request):
    if request.method == "POST":
        Trajectory.objects.create(
            user=request.user,
            job_position=request.POST.get("job_position"),
            description=request.POST.get("description"),
            date_start=request.POST.get("date_start"),
            date_end=request.POST.get("date_end"),
        )
    return redirect("edit_profile")

def edit_trajectory(request, trajectory_id):
    trajectory = get_object_or_404(Trajectory, id=trajectory_id, user=request.user)
    if request.method == "POST":
        trajectory.job_position = request.POST.get("job_position")
        trajectory.description = request.POST.get("description")
        trajectory.date_start = request.POST.get("date_start")
        trajectory.date_end = request.POST.get("date_end")
        trajectory.save()
    return redirect("edit_profile")

def delete_trajectory(request, trajectory_id):
    trajectory = get_object_or_404(Trajectory, id=trajectory_id, user=request.user)
    trajectory.delete()
    return redirect("edit_profile")


# views.py

from django.http import JsonResponse
from adminprofile.models import GithubRepository


def github_repos_api(request):

    repos = GithubRepository.objects.all().values()

    return JsonResponse(
        list(repos),
        safe=False
    )
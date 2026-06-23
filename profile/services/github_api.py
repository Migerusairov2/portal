import os
import requests
from dotenv import load_dotenv
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
from django.contrib.auth.models import User 
from profile.models import Profile

load_dotenv()

<<<<<<< Updated upstream
# superuser = User.objects.filter(is_superuser=True).first()
# profile, created = Profile.objects.get_or_create(user=superuser)

# TOKEN = f'{profile.github_token}'

# if not TOKEN:
#     raise ValueError("GITHUB_TOKEN is not set in .env file or Github Token is expired!")

# headers = {
#     "Authorization": f"Bearer {TOKEN}",
#     "Accept": "application/vnd.github+json"
# }

def get_headers(user):

    profile, created = Profile.objects.get_or_create(user=user)

    token = profile.github_token

    if not token:
        raise ValueError("GitHub token is missing.")

    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }


def fetch_personal_repositories(user):

    headers = get_headers(user)
=======
superuser = User.objects.filter(is_superuser=True).first()
profile, created = Profile.objects.get_or_create(user=superuser)

TOKEN = f'{profile.github_token}'

if not TOKEN:
    raise ValueError("GITHUB_TOKEN is not set in .env file or Github Token is expired!")

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}


def fetch_personal_repositories():
>>>>>>> Stashed changes

    url = "https://api.github.com/user/repos"

    params = {
        "visibility": "all",
        "sort": "updated",
        "per_page": 100
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=10
    )

    return response.json()

GITHUB_API = "https://api.github.com"

<<<<<<< Updated upstream
def fetch_commits(user, owner, repo):
    headers = get_headers(user)
=======
def fetch_commits(owner, repo):
>>>>>>> Stashed changes
    url = f"{GITHUB_API}/repos/{owner}/{repo}/commits?per_page=100"
    r = requests.get(url, headers=headers, timeout=30)

    if r.status_code != 200:
        return []

    return r.json()
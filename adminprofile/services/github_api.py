import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN")

if not TOKEN:
    raise ValueError("GITHUB_TOKEN is not set in .env file or Github Token is expired!")

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}


def fetch_personal_repositories():

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

def fetch_commits(owner, repo):
    url = f"{GITHUB_API}/repos/{owner}/{repo}/commits?per_page=100"
    r = requests.get(url, headers=headers, timeout=30)

    if r.status_code != 200:
        return []

    return r.json()
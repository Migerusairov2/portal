from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from profile.services.github_api import (
    fetch_personal_repositories,
    fetch_commits
)
from profile.models import GithubRepository, GithubCommit


class Command(BaseCommand):

    help = "Sync GitHub repositories and commits"

    def add_arguments(self, parser):
        parser.add_argument('--user_id', type=int)

    def handle(self, *args, **kwargs):

        user_id = kwargs.get('user_id')

        if not user_id:
            self.stdout.write(
                self.style.ERROR("user_id is required")
            )
            return

        user = User.objects.get(id=user_id)

        self.stdout.write(self.style.SUCCESS(f"Syncing for user: {user.username}"))

        repositories = fetch_personal_repositories(user)

        # print("REPOSITORIES:", repositories)  # DEBUG

        for repo in repositories:
            print('repo["name"]', repo["name"])

            repo_obj, _ = GithubRepository.objects.update_or_create(
                user=user,
                repo_url=repo["html_url"],
                defaults={
                    "name": repo["name"],
                    "owner": repo["owner"]["login"],
                    "stars": repo["stargazers_count"],
                    "language": repo["language"] or "",
                    "description": repo["description"] or "",
                    "pushed_at": repo["pushed_at"],
                }
            )

            commits = fetch_commits(
                user,
                repo["owner"]["login"],
                repo["name"]
            )

            for c in commits:

                commit_data = c.get("commit", {})
                author = commit_data.get("author", {}) or {}

                GithubCommit.objects.update_or_create(
                    repo=repo_obj,
                    sha=c["sha"],
                    defaults={
                        "message": commit_data.get("message", ""),
                        "author": author.get("name", ""),
                        "date": author.get("date"),
                        "url": c.get("html_url", ""),
                    }
                )

        self.stdout.write(self.style.SUCCESS("Sync complete"))
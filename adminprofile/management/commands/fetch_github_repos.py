# management/commands/sync_github.py

from django.core.management.base import BaseCommand
from adminprofile.services.github_api import (
    fetch_personal_repositories,
    fetch_commits
)
from adminprofile.models import GithubRepository, GithubCommit


class Command(BaseCommand):

    help = "Sync GitHub repositories and commits"

    def handle(self, *args, **kwargs):

        repositories = fetch_personal_repositories()
        # print("---",repositories)

        for repo in repositories:

            repo_obj, _ = GithubRepository.objects.update_or_create(
                repo_url=repo["html_url"],
                defaults={
                    "name": repo["name"],
                    "owner": repo["owner"]["login"],
                    "stars": repo["stargazers_count"],
                    "language": repo["language"] or "",
                    "description": repo["description"] or "",
                    "pushed_at" : repo["pushed_at"],
                }
            )

            self.stdout.write(self.style.SUCCESS(
                f"Repo saved: {repo['name']}"
            ))

            commits = fetch_commits(repo["owner"]["login"], repo["name"])

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

            self.stdout.write(self.style.SUCCESS(
                f"Commits synced: {repo['name']}"
            ))
from django.urls import path
from . import views
from profile.api.api import github_repos_api

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path("api/github-repos/", github_repos_api, name="github_repos_api"),
    path("api/sync-github/", views.sync_github, name="sync_github"),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
]




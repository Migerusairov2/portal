from django.urls import path
from . import views
from profile.api.api import github_repos_api

urlpatterns = [
    path('overview/', views.admin_profile, name='overview'),
    path("api/github-repos/", github_repos_api, name="github_repos_api"),
]




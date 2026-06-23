from django.urls import path
from . import views
from profile.api.api import github_repos_api

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path("api/github-repos/", github_repos_api, name="github_repos_api"),
    path("api/sync-github/", views.sync_github, name="sync_github"),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('social-media/delete/<int:id>/', views.delete_social_media, name='delete_social_media'),
    path('social-media/add/', views.add_social_media, name='add_social_media'),
    path(
    "remove-framework/<int:id>/",
    views.remove_framework,
    name="remove_framework"
    ),
    path(
        "add-framework/",
        views.add_framework,
        name="add_framework"
    ),

    path(
        'add-language/',
        views.add_language,
        name='add_language'
    ),
]




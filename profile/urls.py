from django.urls import path
from . import views
from profile.api.api import github_repos_api

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path("api/github-repos/", github_repos_api, name="github_repos_api"),
    path("api/sync-github/", views.sync_github, name="sync_github"),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    path('social-media/add/', views.add_social_media, name='add_social_media'),
    path('social-media/delete/<int:id>/', views.delete_social_media, name='delete_social_media'),
    
    path("add-framework/", views.add_framework, name="add_framework"),
    path("remove-framework/<int:id>/", views.remove_framework, name="remove_framework"),

    path('add-language/', views.add_language, name='add_language'),
    path("remove-language/<int:language_id>/", views.remove_language, name="remove_language"),

    path('add-project/', views.add_project, name='add_project'),
    path("edit-project/<int:project_id>/", views.edit_project, name="edit_project"),
    path('project/<int:project_id>/delete/', views.delete_project, name='delete_project'),

    path("add-trajectory/", views.add_trajectory, name="add_trajectory"),
    path("edit-trajectory/<int:trajectory_id>/", views.edit_trajectory, name="edit_trajectory"),
    path("delete-trajectory/<int:trajectory_id>/", views.delete_trajectory, name="delete_trajectory"),

]




from django.contrib import admin
from .models import Profile, Language, Project, Framework, Trajectory, SocialMedia, ProjectImage, GithubRepository

@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'logo', 'user')
    list_filter = ('user',)

@admin.register(Trajectory)
class TrajectoryAdmin(admin.ModelAdmin):
    list_display = ('job_position', 'date_start', 'date_end', 'description', 'user')
    list_filter = ('user',)


@admin.register(Framework)
class FrameworkAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo')

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'color_code')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'url' , 'pinned', 'user')
    list_filter = ('pinned', 'user')
    filter_horizontal = ('languages_used',)

@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'caption', 'project')
 
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'profile', 'description', 'github_token']
    filter_horizontal = ('languages', 'frameworks',)

@admin.register(GithubRepository)
class GithubRepositoryAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'owner',
        'stars',
        'language',
        'user'

    )

    list_filter = ('user',)


    search_fields = (
        'name',
        'owner'
    )


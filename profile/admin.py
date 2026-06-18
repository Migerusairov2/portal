from django.contrib import admin
from .models import Profile, Language, Project, Framework, Trajectory, SocialMedia, ProjectImage, GithubRepository

@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ('user','name', 'url', 'logo')
    list_filter = ('user',)

@admin.register(Trajectory)
class TrajectoryAdmin(admin.ModelAdmin):
    list_display = ('user','job_position', 'date_start', 'date_end', 'description')
    list_filter = ('user',)


@admin.register(Framework)
class FrameworkAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo')

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'color_code')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'description', 'url' , 'pinned')
    list_filter = ('pinned', 'user')
    filter_horizontal = ('languages_used',)

@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ('project', 'image', 'caption')
 
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'description', 'profile', 'github_token']
    filter_horizontal = ('languages', 'frameworks',)

@admin.register(GithubRepository)
class GithubRepositoryAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'owner',
        'stars',
        'language'
    )

    search_fields = (
        'name',
        'owner'
    )
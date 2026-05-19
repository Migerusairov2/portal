from django.db import models
from django.contrib.auth.models import User

class Framework(models.Model):
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='logo/', blank=True)

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=50)
    color_code = models.CharField(max_length=7, default="#cccccc") # e.g., #f1e05a

    def __str__(self):
        return self.name
    
class SocialMedia(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_media')
    logo = models.ImageField(upload_to='logo/', blank=True)
    name = models.CharField(max_length=50)
    url = models.URLField(max_length=255, blank=True, default='')

    def __str__(self):
        return self.name
    
class Trajectory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trajectories')
    job_position = models.CharField(max_length=50)
    date_start= models.DateField(blank=True)
    date_end= models.DateField(blank=True)
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.job_position
    
class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500, blank=True)
    languages_used = models.ManyToManyField(Language, blank=True)
    pinned = models.BooleanField(default=False)
    url = models.URLField(max_length=255, blank=True, default='')
    
    def __str__(self):
        return self.name
    
class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='project_previews/')
    caption = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.project.name} Image"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=500, null=True, blank=True)
    frameworks = models.ManyToManyField(Framework, blank=True)
    languages = models.ManyToManyField(Language, blank=True)
    # projects = models.ManyToManyField(Project, blank=True)
    profile = models.ImageField(upload_to='profile/', null=True, blank=True)
    trajectories = models.ManyToManyField(Trajectory, blank=True)
    social_medias = models.ManyToManyField(SocialMedia, blank=True)

    
    def __str__(self):
        return self.user.username
    
from django.db import models


class GithubRepository(models.Model):

    name = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    repo_url = models.URLField(unique=True)
    stars = models.IntegerField(default=0)
    language = models.CharField(
        max_length=100,
        blank=True
    )
    description = models.TextField(blank=True)
    pushed_at = models.DateTimeField(blank=True)

    def __str__(self):
        return self.name
    
class GithubCommit(models.Model):
    repo = models.ForeignKey(
        GithubRepository,
        on_delete=models.CASCADE,
        related_name="commits"
    )

    sha = models.CharField(max_length=100)
    message = models.TextField()
    author = models.CharField(max_length=255, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    url = models.URLField()

    class Meta:
        unique_together = ("repo", "sha")  # IMPORTANT FIX

    def __str__(self):
        return f"{self.repo.name} - {self.sha[:7]}"
from django.db import models
from django.contrib.auth.models import User


class Source(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Training(models.Model):
    source = models.ForeignKey(
        Source,
        on_delete=models.CASCADE,
        related_name='trainings'
    )

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} ({self.source.name})"

class Certificate(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='certificates'
    )

    training = models.ForeignKey(
        Training,
        on_delete=models.CASCADE,
        related_name='certificates'
    )

    caption = models.CharField(max_length=100)

    file = models.ImageField(
        upload_to='certificates/',
        blank=True,
        null=True
    )

    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.training.title}"
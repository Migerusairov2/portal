from django.contrib import admin
from django import forms
from .models import Training, Certificate, Source, Guide

@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ('name', 'url',)


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ('title', 'source')
    list_filter = ('source',)
    search_fields = ('title',)


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('user', 'training', 'caption', 'issued_at')
    list_filter = ('training', 'user')
    search_fields = ('user_username', 'training_title', 'caption')

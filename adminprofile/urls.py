from django.urls import path
from . import views

urlpatterns = [
    path('overview/', views.admin_profile, name='overview'),       
]




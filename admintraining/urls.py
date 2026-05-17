from django.urls import path
from . import views

urlpatterns = [
    path('trainings/', views.trainings, name='trainings'),       
]




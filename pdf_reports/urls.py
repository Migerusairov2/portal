from django.urls import path
from .views import pdf_report

urlpatterns = [
    path('pdf-report/', pdf_report, name='pdf_report'),
]
from django.shortcuts import render
from django.contrib.auth.models import User


def trainings(request):

    superuser = User.objects.filter(is_superuser=True).first()
    superuser_certificates = superuser.certificates.select_related('training')

    context = {
        'user': superuser,
        'certificates': superuser_certificates,
    }

    return render(request, 'trainings.html', context)
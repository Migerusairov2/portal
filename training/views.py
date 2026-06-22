from django.shortcuts import render
from django.contrib.auth.models import User
from collections import defaultdict
from pprint import pprint
from .models import Guide
from django.http import HttpResponse



def trainings(request):

    if request.user.is_authenticated:
        user = request.user
    else:
        user = User.objects.filter(is_superuser=True).first()

        if not user:
            return HttpResponse("No superuser found.")


    trainings = user.certificates.select_related('training').order_by('-issued_at')

    grouped_trainings = defaultdict(list)
    guides = Guide.objects.all()

    for cert in trainings:
        grouped_trainings[cert.training.source].append({
            'title': cert.training.title,
            'issued_at': cert.issued_at,
            'description': cert.training.description,
            'certificate_file': cert.file
        })

    # pprint(grouped_trainings, sort_dicts=False)

    context = {
        'user': user,
        'grouped_trainings': dict(grouped_trainings),
        'guides': guides
    }

    return render(request, 'trainings.html', context)
from django.shortcuts import render
from .models import Pitch


def pitches(request):
    """
    A view that renders map page and provides all pitches to map
    """

    pitches = Pitch.objects.all()
    template = 'pitches/pitches.html'
    context = {
        'pitches': pitches,
    }

    return render(request, template, context)

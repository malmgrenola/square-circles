from django.shortcuts import render
from .models import Pitch


def pitches(request):
    """A view that renders map page"""
    template = 'pitches/pitches.html'

    pitches = Pitch.objects.all()

    context = {
        'pitches': pitches,
    }

    return render(request, template, context)

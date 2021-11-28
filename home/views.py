from django.shortcuts import render


def index(request):
    """A view that renders index page"""

    return render(request, 'home/home.html')

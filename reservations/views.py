from django.shortcuts import render, redirect, reverse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.db.models import Q


@require_http_methods(["GET"])
def reservations(request):
    """ render reservations view """

    context = {
    }
    return render(request, 'reservations/reservations.html', context)

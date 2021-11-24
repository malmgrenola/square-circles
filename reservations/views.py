from django.shortcuts import render, redirect, reverse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.db.models import Q


@require_http_methods(["GET"])
def reservations(request):
    """ render reservations view """

    context = {
    }
    return render(request, 'reservations/reservations.html', context)


@require_http_methods(["POST"])
def set_availability(request):
    """ set availability parameters to session """

    availability = {
        'start': request.POST.get('startDate'),
        'end': request.POST.get('endDate')
    }

    request.session['availability'] = availability

    return HttpResponse(status=200)

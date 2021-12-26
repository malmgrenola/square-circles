from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import Review
from datetime import datetime


@require_http_methods(["GET"])
def reviews(request):
    """
    A view that renders reviews page.
    """

    reviews = Review.objects.all()

    context = {
        'reviews': reviews,
    }

    return render(request, 'reviews/reviews.html', context)

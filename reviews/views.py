from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from .forms import ReviewForm
from profiles.models import UserProfile


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


@require_http_methods(["GET", "POST"])
@login_required()
def change(request, review_id):
    """
    A view that handles review changes and delete redirect.
    """
    review = get_object_or_404(Review, id=review_id)

    if request.method == 'POST':
        if '_delete' in request.POST:
            return redirect('delete', review_id)

        review_form = ReviewForm(request.POST, instance=review)
        if review_form.is_valid():
            review = review_form.save()
            messages.success(
                request, f'Review successfully changed')
            return redirect(reverse('profile'))

        else:
            messages.error(
                request, f'Unable to change review')
    else:
        review_form = ReviewForm(instance=review)

    context = {
        'review_form': review_form,
        'review_id': review_id,
    }

    return render(request, 'reviews/review.html', context)


@require_http_methods(["GET", "POST"])
@login_required()
def add(request):
    """
    A view that creates a new review.
    """

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.profile = UserProfile.objects.get(
                user=request.user) if request.user.is_authenticated else None
            review.save()

            messages.success(
                request, f'Review successfully added')
            return redirect(reverse('profile'))

        else:
            messages.error(
                request, f'Unable to add review')

        return redirect(reverse('add'))

    review_form = ReviewForm()

    context = {
        'review_form': review_form
    }

    return render(request, 'reviews/add.html', context)


@require_http_methods(["GET", "POST"])
@login_required()
def delete(request, review_id):
    """
    A 'Are you sure to delete' view that also handles abort
    """
    review = get_object_or_404(Review, id=review_id)

    if '_abort' in request.POST:
        return redirect('change', review.id)

    if '_do' in request.POST:
        review.delete()
        messages.success(
            request, f'Review successfully deleted')
        return redirect('profile')

    context = {
        'review': review,
    }

    return render(request, 'reviews/delete.html', context)

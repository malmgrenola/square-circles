from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import UserProfile
from .forms import UserProfileForm, UserForm
from django.contrib.auth.models import User
from checkout.models import Order


@require_http_methods(["GET", "POST"])
@login_required
def profile(request):
    """
    Display the user's profile with forms needed for update and order history.
    """

    profile = get_object_or_404(UserProfile, user=request.user)
    user = get_object_or_404(User, username=request.user)
    orders = profile.orders.all()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        user_form = UserForm(request.POST, instance=user)
        if form.is_valid() and user_form.is_valid():
            form.save()
            user_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(
                request, 'Update failed. Please ensure the form is valid.')
    else:
        form = UserProfileForm(instance=profile)
        user_form = UserForm(instance=user)
    template = 'profiles/profile.html'
    context = {
        'form': form,
        'user': user,
        'user_form':  user_form,
        'orders': orders,

    }

    return render(request, template, context)


def order_history(request, order_number):
    """
    Fetch and render a single order done in the past.
    """
    order = get_object_or_404(Order, order_number=order_number)
    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)

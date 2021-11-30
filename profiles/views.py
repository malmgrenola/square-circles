from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import UserProfile
from .forms import UserProfileForm, UserForm
from django.contrib.auth.models import User


@require_http_methods(["GET", "POST"])
@login_required
def profile(request):
    """ Display the user's profile. """

    profile = get_object_or_404(UserProfile, user=request.user)
    user = get_object_or_404(User, username=request.user)

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
        'user_form':  user_form
    }

    return render(request, template, context)

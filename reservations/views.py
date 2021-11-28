from django.shortcuts import render, redirect, reverse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import Reservation
from products.models import Product
from django.db.models import Q
from .forms import ReservationForm


@require_http_methods(["GET", "POST"])
def reservation(request):
    """ render reservations view and handle create reservations"""

    return render(request, 'reservations/reservations.html')


@require_http_methods(["GET"])
def add_reservation(request, product_id):

    product = get_object_or_404(Product, pk=product_id)
    reservations = request.session.get('reservations', [])
    travel_info = request.session.get('travel_info', {})
    check_in = None
    check_out = None

    if 'check_in' in travel_info and 'check_out' in travel_info:
        check_in = travel_info['check_in']
        check_out = travel_info['check_out']

    reservations.append({
        'product_id': product_id,
        'check_in': check_in,
        'check_out': check_out, })

    request.session['reservations'] = reservations
    messages.success(
        request, f'Successfully added {product.name} to your reservations')

    return redirect(reverse('reservation'))


@require_http_methods(["GET"])
def remove_reservation(request, reservation_index):

    # product = get_object_or_404(Product, pk=product_id)
    reservations = request.session.get('reservations', [])

    if reservations:
        if reservation_index <= len(reservations):
            product_id = reservations[reservation_index]['product_id']
            product = get_object_or_404(Product, pk=product_id)
            del reservations[reservation_index]
            request.session['reservations'] = reservations
            messages.success(request, f'Successfully removed {product.name}')

    return redirect(reverse('reservation'))


@ require_http_methods(["POST"])
def set_travel_info(request):
    """ set user travel information to current session """

    if 'check_in' in request.POST and 'check_out' in request.POST:
        travel_info = {
            'check_in': request.POST.get('check_in'),
            'check_out': request.POST.get('check_out')
        }
        request.session['travel_info'] = travel_info

        if 'reservations' in request.session:
            # Update all reservations with new travel information
            reservations = request.session['reservations']
            for reservation in reservations:
                reservation['travel_info'] = travel_info
            request.session['reservations'] = reservations

    else:
        messages.error(request, f'Unable to set your travel information')

    return HttpResponse(status=200)

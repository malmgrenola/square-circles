from products.models import Product
from django.shortcuts import get_object_or_404
from datetime import date, datetime


def reservations_contents(request):

    reservations = request.session.get('reservations', [])
    travel_info = request.session.get('travel_info', {})
    reservations_grand_total = 0
    nights = 0

    if 'check_in' in travel_info and 'check_out' in travel_info:
        date_format = "%Y-%m-%d"
        _delta = datetime.strptime(
            travel_info['check_out'], date_format) - datetime.strptime(travel_info['check_in'], date_format)
        nights = _delta.days
        travel_info['nights'] = nights

    for reservation in reservations:
        product = get_object_or_404(Product, pk=reservation['product_id'])

        reservation['total'] = float(nights * product.price)
        reservation['product'] = product
        if nights > 0:
            reservation['travel_info'] = travel_info
        else:
            reservation['travel_info'] = {'nights': 0}

        reservations_grand_total = float(reservations_grand_total +
                                         reservation['total'])

    context = {
        'reservations': reservations,
        'reservations_grand_total': reservations_grand_total,
        'travel_info': travel_info
    }

    return context

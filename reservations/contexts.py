from products.models import Product
from django.shortcuts import get_object_or_404
from datetime import datetime


def reservations_contents(request):

    reservations = request.session.get('reservations', [])
    travel_info = request.session.get('travel_info', {})
    reservations_grand_total = 0
    nights = 0
    amount = 1
    date_format = "%Y-%m-%d"
    reservation_items = []

    if 'check_in' in travel_info and 'check_out' in travel_info:
        _delta = datetime.strptime(
            travel_info['check_out'], date_format) - datetime.strptime(travel_info['check_in'], date_format)
        nights = _delta.days
        travel_info['nights'] = nights

    for reservation in reservations:
        product = get_object_or_404(Product, pk=reservation['product_id'])
        check_in = reservation['check_in']
        check_out = reservation['check_out']
        nights = (datetime.strptime(
            check_out, date_format) - datetime.strptime(check_in, date_format)).days
        total = float(amount * nights * product.price)
        reservation_items.append({
            'product': product,
            'amount': amount,
            'total': total,
            'check_in': check_in,
            'check_out': check_out,
            'nights': nights
        })
        reservations_grand_total = float(reservations_grand_total + total)

    context = {
        'reservation_items': reservation_items,
        'reservations_grand_total': reservations_grand_total,
        'travel_info': travel_info
    }

    return context

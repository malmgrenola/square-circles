from products.models import Product
from django.shortcuts import get_object_or_404
from datetime import datetime
from products.views import product_available


def basket_contents(request):

    basket = request.session.get('basket', [])
    travel_info = request.session.get('travel_info', {})
    basket_grand_total = 0
    days = 0

    date_format = "%Y-%m-%d"
    basket_items = []

    if 'check_in' in travel_info and 'check_out' in travel_info:
        travel_info['days'] = (datetime.strptime(
            travel_info['check_out'], date_format) - datetime.strptime(travel_info['check_in'], date_format)).days

    for item in basket:
        product = get_object_or_404(Product, pk=item['product_id'])
        check_in = datetime.strptime(
            item['check_in'], '%Y-%m-%d')
        check_out = datetime.strptime(
            item['check_out'], '%Y-%m-%d')
        quantity = item['quantity']
        days = item['days']
        total = float(quantity * days * product.price)
        basket_items.append({
            'product': product,
            'quantity': quantity,
            'total': total,
            'check_in': check_in,
            'check_out': check_out,
            'days': days,
            'available': product_available(product, check_in, check_out)
        })
        basket_grand_total = float(basket_grand_total + total)

    context = {
        'basket_items': basket_items,
        'basket_grand_total': basket_grand_total,
        'travel_info': travel_info
    }

    return context

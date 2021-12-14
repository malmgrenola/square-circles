from django.shortcuts import render, redirect, reverse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.contrib import messages
from products.models import Product
from datetime import datetime
from products.views import product_available


@require_http_methods(["GET", "POST"])
def basket(request):
    """ render basket view and handle create reservations"""

    return render(request, 'basket/basket.html')


@require_http_methods(["GET"])
def add_product(request, product_id):

    product = get_object_or_404(Product, pk=product_id)
    basket = request.session.get('basket', [])
    travel_info = request.session.get('travel_info', {})
    check_in = None
    check_out = None

    if 'check_in' in travel_info and 'check_out' in travel_info:
        check_in = travel_info['check_in']
        check_out = travel_info['check_out']

    if not check_in or not check_out:
        messages.error(
            request, f'You must add availability information on when you would like to book')
        return redirect(reverse('basket'))

    available = product_available(product, datetime.strptime(
        check_in, '%Y-%m-%d'), datetime.strptime(
        check_out, '%Y-%m-%d'))

    item = None
    i = 0
    for x in basket:
        if x['product_id'] == product_id and x['check_in'] == check_in and x['check_out'] == check_out:
            if available - x['quantity'] <= 0:
                messages.error(
                    request, f'{product} is not available in the selected period.')
                return redirect(reverse('basket'))
            item = x
            break
        i += 1

    if item:
        basket[i]['quantity'] += 1
    else:
        date_format = "%Y-%m-%d"
        basket.append({
            'product_id': product_id,
            'check_in': check_in,
            'check_out': check_out,
            'days': (datetime.strptime(
                check_out, date_format) - datetime.strptime(check_in, date_format)).days,
            'quantity': 1
        })

    request.session['basket'] = basket
    messages.success(
        request, f'Successfully added {product.name} to your basket')

    return redirect(reverse('basket'))


@require_http_methods(["POST"])
def update_item(request, basket_index):
    """Update basket item based on basket index """

    basket = request.session.get('basket', [])

    cmd_add = request.POST.get('add', None)
    cmd_remove = request.POST.get('remove', None)

    if basket and basket_index <= (len(basket)-1):
        product_id = basket[basket_index]['product_id']
        product = get_object_or_404(Product, pk=product_id)
        quantity = basket[basket_index]['quantity']
        check_in = datetime.strptime(
            basket[basket_index]['check_in'], '%Y-%m-%d')
        check_out = datetime.strptime(
            basket[basket_index]['check_out'], '%Y-%m-%d')
        available = product_available(product, check_in, check_out)

        if cmd_add == '+':
            # limit max bookings
            if quantity < available:
                quantity += 1
            else:
                messages.error(
                    request, f'It is not possible to reserve {product.name}')
                return redirect(reverse('basket'))

        if cmd_remove == '-' and quantity > 1:
            quantity -= 1

        basket[basket_index]['quantity'] = quantity
        request.session['basket'] = basket
        messages.success(request, f'Successfully updated {product.name}')
    else:
        messages.error(request, f'Not possible to update basket')

    return redirect(reverse('basket'))


@require_http_methods(["GET"])
def remove_product(request, basket_index):
    """Removes basket item based on basket index """

    basket = request.session.get('basket', [])

    if basket:
        if basket_index <= len(basket):
            product_id = basket[basket_index]['product_id']
            product = get_object_or_404(Product, pk=product_id)
            del basket[basket_index]
            request.session['basket'] = basket
            messages.success(request, f'Successfully removed {product.name}')

    return redirect(reverse('basket'))


@ require_http_methods(["POST"])
def set_travel_info(request):
    """ set user travel information to current session """

    basket = request.session.get('basket', [])
    basket_index = request.POST.get('basket_index', None)
    check_in = request.POST.get('check_in', None)
    check_out = request.POST.get('check_out', None)
    previous_travel_info = request.session.get('travel_info', {})

    if not check_in or not check_out:
        messages.error(request, f'Unable to set your travel information')
        return HttpResponse(status=200)

    if basket_index and basket:
        # User would like to change one basket row
        date_format = "%Y-%m-%d"
        basket[int(basket_index)]['check_in'] = check_in
        basket[int(basket_index)]['check_out'] = check_out
        basket[int(basket_index)]['days'] = (datetime.strptime(
            check_out, date_format) - datetime.strptime(check_in, date_format)).days
        request.session['basket'] = basket
    else:
        # User would like to change Global travel
        request.session['travel_info'] = {
            'check_in': check_in,
            'check_out': check_out
        }

        # Update all basket items with new travel information if the previous date was the same
        date_format = "%Y-%m-%d"
        for item in basket:
            if item['check_in'] == previous_travel_info['check_in'] and item['check_out'] == previous_travel_info['check_out']:
                item['check_in'] = check_in
                item['check_out'] = check_out
                item['days'] = (datetime.strptime(
                    check_out, date_format) - datetime.strptime(check_in, date_format)).days

        request.session['basket'] = basket

        messages.success(request, f'Travel information updated')

    # Always return happyness, Errors are displayed in messages
    return HttpResponse(status=200)

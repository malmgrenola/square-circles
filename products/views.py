from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category
from pitches.models import Pitch
from checkout.models import OrderLineItem
from datetime import datetime, timedelta


@require_http_methods(["GET"])
def all_products(request):
    """
    A view that renders products page & handles queries
    """

    products = Product.objects.all()

    query = ""
    categories = Category.objects.filter(id__in=products.values_list('id'))
    sort = ""

    if 'sort' in request.GET:
        sort = request.GET['sort']
        data = sort.split(":", 1)

        # Parse sort data into field and sort direction
        field = data[1] if len(data) == 2 else data[0]
        direction = "-" if len(data) == 2 and data[0] == "desc" else ""

        try:
            # Only validated fields can be sorted
            if (not field == "price" and not field == "name" and not field == "category"):
                raise ValueError

            products = products.order_by(f'{direction}{field}')
        except:
            # Triggers when user tamper with url manually... in a non suppoorted way!
            messages.error(request, "There is an error sorting your data!")
            return redirect(reverse('products'))

    if 'c' in request.GET:
        categories = request.GET['c'].split(',')
        lookup_products = Q()
        lookup_categories = Q()

        # Case insensetive filtering
        for category in categories:
            lookup_products |= Q(category__name__iexact=category)
            lookup_categories |= Q(name__iexact=category)

        products = products.filter(lookup_products)
        categories = Category.objects.filter(lookup_categories)

    if 'q' in request.GET:
        query = request.GET['q']
        if not query:
            messages.error(
                request, "To find products you must supply a query!")
            return redirect(reverse('products'))

        queries = Q(name__icontains=query) | Q(description__icontains=query)
        products = products.filter(queries)

    travel_info = request.session.get('travel_info', {})

    if not travel_info == {}:
        q_check_in = datetime.strptime(travel_info['check_in'], '%Y-%m-%d')
        q_check_out = datetime.strptime(travel_info['check_out'], '%Y-%m-%d')

    for product in products:

        if not travel_info == {}:
            product.available = product_available(
                product, q_check_in, q_check_out)
        else:
            product.available = 0

        product.save()

    context = {
        'products': products,
        'query': query,
        'categories': categories,
        'sort': sort
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """
    A view to show individual product details
    """

    product = get_object_or_404(Product, pk=product_id)

    travel_info = request.session.get('travel_info', {})

    if not travel_info == {}:
        q_check_in = datetime.strptime(travel_info['check_in'], '%Y-%m-%d')
        q_check_out = datetime.strptime(travel_info['check_out'], '%Y-%m-%d')

    if not travel_info == {}:
        product.available = product_available(
            product, q_check_in, q_check_out)
    else:
        product.available = 0

    product.save()

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)


def product_available(product, check_in, check_out):
    """
    Returns the amount of available pitches for a product based on what is ordered
    """

    reserved = 0
    total = Pitch.objects.filter(
        product=product.id).count()
    queries = Q(product=product.id) & (Q(check_in__range=(check_in, check_out + timedelta(days=-1))) | Q(
        check_out__range=(check_in + timedelta(days=1), check_out)))
    for e in OrderLineItem.objects.filter(queries):
        reserved += e.quantity

    return total - reserved

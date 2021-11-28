from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category, Pitch_assign
from reservations.models import Reservation
from datetime import datetime, timedelta


@require_http_methods(["GET"])
def all_products(request):
    """A view that renders products page & handles queries"""

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

    availability = request.session.get('availability', {})

    if not availability == {}:
        q_check_in = datetime.strptime(availability['start'], '%Y-%m-%d')
        q_check_out = datetime.strptime(availability['end'], '%Y-%m-%d')

        for product in products:
            total = Pitch_assign.objects.filter(
                product=product.id).count()

            queries = Q(product=product.id) & (Q(check_in__range=(q_check_in, q_check_out + timedelta(days=-1))) | Q(
                check_out__range=(q_check_in + timedelta(days=1), q_check_out)))

            reserved = Reservation.objects.filter(queries).count()

            product.available = total - reserved
            product.save()

    context = {
        'products': products,
        'query': query,
        'categories': categories,
        'sort': sort
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)

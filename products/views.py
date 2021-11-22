from django.shortcuts import render, redirect, reverse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category


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

    context = {
        'products': products,
        'query': query,
        'categories': categories,
        'sort': sort
    }

    return render(request, 'products/products.html', context)

from django.shortcuts import render, redirect, reverse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.db.models import Q
from .models import Product

@require_http_methods(["GET"])
def all_products(request):
    """A view that renders products page & handles queries"""

    products = Product.objects.all()
    query = ""

    if 'q' in request.GET:
        query = request.GET['q']
        if not query:
            messages.error(request, "To find products you must supply a query!")
            return redirect(reverse('products'))

        queries = Q(name__icontains=query) | Q(description__icontains=query)
        products = products.filter(queries)


    context = {
        'products': products,
        'query': query,
    }

    return render(request, 'products/products.html', context)
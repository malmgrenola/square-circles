from django.shortcuts import render

# Create your views here.
def products(request):
    """A view that renders index page"""
    
    return render(request, 'products/products.html')
from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.conf import settings
from .forms import OrderForm
from .models import Order, OrderLineItem
from profiles.models import UserProfile
from profiles.forms import UserProfileForm
from products.models import Product
from basket.contexts import basket_contents
from datetime import datetime
import stripe
import json
from products.views import product_available


@require_http_methods(["POST"])
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_API_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'basket': json.dumps(request.session.get('basket', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


@require_http_methods(["GET", "POST"])
def checkout(request):
    """ A view that renders the checkout page """

    basket = request.session.get('basket', [])
    date_format = "%Y-%m-%d"

    if request.method == 'POST':
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
        }
        order_form = OrderForm(form_data)
        basket_items_available = is_basket_available(basket)
        if order_form.is_valid() and basket_items_available:
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_basket = json.dumps(basket)
            order.save()
            for item in basket:
                product = Product.objects.get(id=item['product_id'])

                order_line_item = OrderLineItem(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    check_in=datetime.strptime(
                        item['check_in'], date_format),
                    check_out=datetime.strptime(
                        item['check_out'], date_format),
                )
                order_line_item.save()

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(
                request, "It is not possible to process your request")
            return redirect(reverse('basket'))
    else:
        if not basket:
            messages.error(
                request, "There's nothing in your basket at the moment")
            return redirect(reverse('home'))

        current_basket = basket_contents(request)
        grand_total = current_basket['basket_grand_total']
        stripe_total = round(grand_total * 100)

        if stripe_total == 0:
            messages.error(
                request, "There is nothing to charge the card")
            return redirect(reverse('basket'))

        stripe.api_key = settings.STRIPE_API_KEY
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
            payment_method_types=['card'],
        )

        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.default_phone_number,
                })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()
        context = {
            'order_form': order_form,
            'client_secret': intent.client_secret,
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        }
        return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    order_line_items = OrderLineItem.objects.filter(order=order)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # Attach the user's profile to the order
        order.user_profile = profile
        order.save()

        # Save the user's info
        if save_info:
            profile_data = {
                'default_phone_number': order.phone_number,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'basket' in request.session:
        del request.session['basket']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'order_line_items': order_line_items,
    }

    return render(request, template, context)


def is_basket_available(basket):
    """ Returns false if product is not available """

    available = True
    for item in basket:
        product = Product.objects.get(id=item['product_id'])
        check_in = datetime.strptime(
            item['check_in'], '%Y-%m-%d')
        check_out = datetime.strptime(
            item['check_out'], '%Y-%m-%d')

        if product_available(product, check_in, check_out) - item['quantity'] < 0:
            available = False
            break

    return available

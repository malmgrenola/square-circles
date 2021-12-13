import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings

from django_countries.fields import CountryField

from products.models import Product
from profiles.models import UserProfile
from datetime import datetime


class Order(models.Model):
    order_number = models.CharField(
        max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True, related_name='orders')
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)

    date = models.DateTimeField(auto_now_add=True)
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    original_basket = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(
        max_length=254, null=False, blank=False, default='')

    def __str__(self):
        return self.order_number

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """

        self.grand_total = self.lineitems.aggregate(Sum('lineitem_total'))[
            'lineitem_total__sum'] or 0
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False,
                              on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(
        Product, null=False, blank=False, on_delete=models.CASCADE)
    check_in = models.DateField(null=True, blank=True)
    check_out = models.DateField(null=True, blank=True)
    days = models.IntegerField(null=False, blank=False, default=0)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the number of days booked.
        """
        if (self.check_out is not None or self.check_in is not None):
            self.days = (self.check_out - self.check_in).days
        else:
            self.days = 0
        self.lineitem_total = self.product.price * self.quantity * self.days
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.product.name} on order {self.order.order_number}'

    def about(self):
        return f'{self.product.name} on order {self.order.order_number} with {self.quantity} pcs and the value {self.lineitem_total}'

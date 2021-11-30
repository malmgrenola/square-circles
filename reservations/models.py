from django.db import models
from products.models import Product
from profiles.models import UserProfile
from checkout.models import Order

import uuid


class Reservation(models.Model):
    reservation_number = models.UUIDField(
        primary_key=True, default=uuid.uuid4().hex.upper(), editable=False)
    product = models.ForeignKey(
        Product, null=False, blank=False, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    check_in = models.DateField(null=False, blank=False)
    check_out = models.DateField(null=False, blank=False)
    user_profile = models.ForeignKey(
        UserProfile, null=True, blank=True, on_delete=models.CASCADE)
    order = models.ForeignKey(
        Order, null=True, blank=True, on_delete=models.CASCADE)

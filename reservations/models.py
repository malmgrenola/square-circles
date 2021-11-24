from django.db import models
from products.models import Product
import uuid


class Reservation(models.Model):
    reservation_number = models.UUIDField(
        primary_key=True, default=uuid.uuid4().hex.upper(), editable=False)
    product = models.ForeignKey(
        Product, null=False, blank=False, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    check_in = models.DateField(null=False, blank=False)
    check_out = models.DateField(null=False, blank=False)

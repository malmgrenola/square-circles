from django.contrib import admin
from . models import Order, OrderLineItem


class OrderLineItemInline(admin.TabularInline):
    model = OrderLineItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderLineItemInline,
    ]

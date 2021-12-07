from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total', 'days',)
    fields = ('quantity', 'product', 'check_in',
              'check_out', 'days', 'lineitem_total',)
    list_display = ('quantity', 'product', 'check_in',
                    'check_out', 'days', 'lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = ('order_number', 'date',
                       'grand_total', 'original_basket',
                       'stripe_pid')

    fields = ('order_number', 'user_profile', 'date', 'full_name',
              'email', 'phone_number',  'grand_total', 'original_basket',
              'stripe_pid')

    list_display = ('order_number', 'date', 'full_name',
                    'grand_total',)

    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)

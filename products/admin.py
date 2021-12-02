from django.contrib import admin
from . models import Product, Category
from pitches.models import Pitch


class PitchesInline(admin.TabularInline):
    model = Pitch


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['category']
    inlines = [
        PitchesInline,
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('friendly_name',
                     'name',)

    list_display = (
        'name',
    )

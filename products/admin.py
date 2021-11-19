from django.contrib import admin
from . models import Product,Category,Pitch_assign


class PitchesInline(admin.TabularInline):
    model = Pitch_assign
    # def get_queryset(self, request):
    #     field = super(PitchesInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
    #     qs = super(PitchesInline, self).get_queryset(request)
    #     if request.user.is_superuser:
    #         print('DUPERUSER')
    #     print('OLA WAS HERE', qs)
    #     return qs.filter(pitch=34)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['category']
    inlines = [
        PitchesInline,
    ]
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('friendly_name',
        'name',)

    list_display = (
        'name',
    )
    pass

@admin.register(Pitch_assign)
class PitchesAdmin(admin.ModelAdmin):
    pass


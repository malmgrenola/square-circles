from django.contrib import admin
from . models import Pitch
from django.db.models import CharField
from django.db.models.functions import Cast


@admin.register(Pitch)
class PitchAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'seasonal',
        'tent',
        'electric',
        'water'
    )

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'seasonal', 'tent', 'product')
        }),
        ('Services', {
            'classes': ('wide', 'extrapretty'),
            'fields': ('electric', 'plug', 'graywaste', 'fullwaste', 'water'),
        }),
    )
    search_fields = ('name', 'description')

    def get_queryset(self, request):
        """ Order pitches by name """

        queryset = super().get_queryset(request).annotate(
            _name_as_number=Cast('name', CharField())).order_by('_name_as_number', 'name',)
        return queryset

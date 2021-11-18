from django.contrib import admin
from . models import Pitch
from django.db.models import IntegerField
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
            'fields': ('name','description','seasonal','tent')
        }),
        ('Services', {
            'classes': ('wide', 'extrapretty'),
            'fields': ('electric', 'plug', 'graywaste','fullwaste', 'water'),
        }),
    )
    search_fields = ('name', 'description')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        
        queryset = queryset.annotate(  
            _name_as_number = Cast('name', IntegerField())).order_by('_name_as_number','name')
        print(queryset)
        return queryset

    def name_as_number(self,obj):
        obj._name_as_number

 
  

    name_as_number.admin_order_field = '_name_as_number'

    pass


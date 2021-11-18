from django.test import TestCase
from .models import Pitch
from .admin import PitchAdmin
from django.contrib import admin
from django.db.models import IntegerField 
from django.db.models.functions import Cast 

class MockRequest:
    pass

request = MockRequest()


class TestModels(TestCase):
    
    def test_electric_defaults_to_false(self):
        item = Pitch.objects.create(name='Test pitch item')
        self.assertFalse(item.electric)


    def test_item_string_method_returns_name(self):
        item = Pitch.objects.create(name='Test pitch item')
        self.assertEqual(str(item), 'Test pitch item')

class TestAdmin(TestCase):
    def test_queryset_override(self):
        item = Pitch.objects.create(name='1A')
        pa = PitchAdmin(Pitch,self).get_queryset(request).annotate(_name_as_number = Cast('name', IntegerField())).order_by('_name_as_number','name')
        self.assertTrue(pa.filter(name=item.name).exists())

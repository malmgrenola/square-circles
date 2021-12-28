from django.contrib import admin
from django.db import models
from . models import Review
from django_starfield import Stars


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.IntegerField: {'widget': Stars},
    }

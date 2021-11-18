from django.db import models


class Pitch(models.Model):
    name = models.CharField(max_length=254)
    description = models.TextField(null=True, blank=True)
    electric = models.BooleanField(default=False, null=True, blank=False)
    plug = models.CharField(max_length=254,null=True, blank=True)
    graywaste = models.BooleanField(default=False, null=True, blank=False)
    fullwaste = models.BooleanField(default=False, null=True, blank=False)
    water = models.BooleanField(default=False, null=True, blank=False)
    tent = models.BooleanField(default=False, null=True, blank=False)
    seasonal = models.BooleanField(default=False, null=True, blank=False)

    def __str__(self):
        return self.name

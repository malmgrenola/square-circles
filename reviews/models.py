from django.db import models
from profiles.models import UserProfile
from django.contrib.humanize.templatetags.humanize import naturaltime


class Review(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                null=True, blank=True)
    name = models.CharField(max_length=50, null=False, blank=False)
    review = models.TextField(null=False, blank=False, default='')
    rating = models.IntegerField(null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'review by {self.name} made {naturaltime(self.date)}'

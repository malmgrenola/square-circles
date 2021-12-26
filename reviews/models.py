from django.db import models
from profiles.models import UserProfile


class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                             null=True, blank=True, related_name='reviews')
    name = models.CharField(max_length=50, null=False, blank=False)
    review = models.TextField(null=False, blank=False, default='')
    rating = models.PositiveSmallIntegerField(null=False, blank=False)
    date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'review by {self.name} made {self.date}'

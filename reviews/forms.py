from django import forms
from .models import Review
from django_starfield import Stars


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review

        fields = ('name', 'review', 'rating',)
        labels = {
            'name': 'Your name',
            'review': 'Review',
            'rating': 'Rating',
        }

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """

        super().__init__(*args, **kwargs)
        placeholders = {
            'name': 'Enter your name',
            'review': 'Write your review',
            'rating': 'Write your rating',
        }

        self.fields['name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field == 'rating':
                self.fields[field] = forms.IntegerField(widget=Stars)
            else:
                self.fields[field].widget.attrs['placeholder'] = placeholders[field]

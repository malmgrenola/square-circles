from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        labels = {
            'default_phone_number': 'Phone number',
            'default_street_address1': 'Street address 1',
            'default_street_address2': 'Street address 2',
            'default_town_or_city': 'Town or City',
            'default_county': 'County',
            'default_postcode': 'Postcode',
            'default_country': 'Country',
        }
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_town_or_city': 'Town or City',
            'default_postcode': 'Postal Code',
            'default_county': 'County, State or Locality',
        }

        self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'default_country':
                placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder

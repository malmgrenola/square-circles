from django import forms
from .models import UserProfile
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        labels = {
            'default_phone_number': 'Phone number',
        }
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes and set autofocus on first field
        """

        super().__init__(*args, **kwargs)
        placeholders = {
            'default_phone_number': 'Phone Number',
        }

        self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        for field in self.fields:
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder

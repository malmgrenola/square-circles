# Generated by Django 3.2.9 on 2021-12-01 08:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='default_country',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='default_county',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='default_postcode',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='default_street_address1',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='default_street_address2',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='default_town_or_city',
        ),
    ]
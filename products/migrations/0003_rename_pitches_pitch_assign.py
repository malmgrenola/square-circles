# Generated by Django 3.2.9 on 2021-11-19 14:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pitches', '0001_initial'),
        ('products', '0002_remove_category_friendly_name'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Pitches',
            new_name='Pitch_assign',
        ),
    ]

# Generated by Django 3.2.9 on 2021-12-25 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_delete_pitch_assign'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image_url',
        ),
    ]

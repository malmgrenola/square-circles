# Generated by Django 3.2.9 on 2021-11-29 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0002_alter_reservation_reservation_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='reservation_number',
            field=models.UUIDField(default='30463A0F585546B0B632B2681ECE8AC6', editable=False, primary_key=True, serialize=False),
        ),
    ]
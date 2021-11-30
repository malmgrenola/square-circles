# Generated by Django 3.2.9 on 2021-11-30 13:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0003_auto_20211130_1352'),
        ('profiles', '0001_initial'),
        ('reservations', '0004_alter_reservation_reservation_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='checkout.order'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='user_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.userprofile'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='reservation_number',
            field=models.UUIDField(default='9DF723CF7B7A43419FE1635B316F4A6D', editable=False, primary_key=True, serialize=False),
        ),
    ]
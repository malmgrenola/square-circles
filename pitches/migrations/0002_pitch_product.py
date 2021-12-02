# Generated by Django 3.2.9 on 2021-12-02 09:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_delete_pitch_assign'),
        ('pitches', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pitch',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.product'),
        ),
    ]

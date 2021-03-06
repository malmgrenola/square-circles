# Generated by Django 3.2.9 on 2021-11-18 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pitch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254)),
                ('description', models.TextField(blank=True, null=True)),
                ('electric', models.BooleanField(default=False, null=True)),
                ('plug', models.CharField(blank=True, max_length=254, null=True)),
                ('graywaste', models.BooleanField(default=False, null=True)),
                ('fullwaste', models.BooleanField(default=False, null=True)),
                ('water', models.BooleanField(default=False, null=True)),
                ('tent', models.BooleanField(default=False, null=True)),
                ('seasonal', models.BooleanField(default=False, null=True)),
            ],
        ),
    ]

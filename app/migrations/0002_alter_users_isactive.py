# Generated by Django 3.2.9 on 2022-01-05 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='isActive',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]

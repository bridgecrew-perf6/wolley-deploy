# Generated by Django 3.0.14 on 2022-02-23 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountapp', '0003_estimate_location_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estimate',
            name='location_id',
            field=models.CharField(default='0', max_length=100),
        ),
    ]
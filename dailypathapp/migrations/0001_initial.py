# Generated by Django 3.0.14 on 2022-01-14 18:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accountapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyPath',
            fields=[
                ('id', models.BigAutoField(db_column='dailypath_id', primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dailypaths', to='accountapp.AppUser')),
            ],
            options={
                'db_table': 'dailypathapp',
            },
        ),
    ]

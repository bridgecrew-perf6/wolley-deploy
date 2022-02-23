# Generated by Django 3.0.14 on 2022-02-23 23:58

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accountapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Diary',
            fields=[
                ('id', models.BigAutoField(db_column='diary_id', primary_key=True, serialize=False)),
                ('date', models.DateField(default=datetime.date.today)),
                ('content', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diarys', to='accountapp.AppUser')),
            ],
            options={
                'db_table': 'diary',
            },
        ),
    ]

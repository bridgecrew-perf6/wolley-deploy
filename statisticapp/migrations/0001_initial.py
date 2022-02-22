# Generated by Django 3.0.14 on 2022-02-20 17:33

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
            name='WeekInfo',
            fields=[
                ('id', models.BigAutoField(db_column='weekinfo_id', primary_key=True, serialize=False)),
                ('year', models.IntegerField(default=1900)),
                ('month_order', models.IntegerField(default=0)),
                ('week_order', models.IntegerField(default=0)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weekinfos', to='accountapp.AppUser')),
            ],
            options={
                'db_table': 'weekinfo',
            },
        ),
        migrations.CreateModel(
            name='WeekCategoryInfo',
            fields=[
                ('id', models.BigAutoField(db_column='weekcategoryinfo_id', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=70)),
                ('date', models.DateTimeField(default=datetime.datetime.today)),
                ('time_spent', models.DurationField(default=datetime.timedelta(seconds=1200))),
                ('percent', models.FloatField(default=0.0)),
                ('rank', models.FloatField(default=0.0)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('week_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weekcategoryinfos', to='statisticapp.WeekInfo')),
            ],
            options={
                'db_table': 'weekcategoryinfo',
            },
        ),
        migrations.CreateModel(
            name='MonthInfo',
            fields=[
                ('id', models.BigAutoField(db_column='monthinfo_id', primary_key=True, serialize=False)),
                ('year', models.IntegerField(default=1900)),
                ('month_order', models.IntegerField(default=0)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='monthinfos', to='accountapp.AppUser')),
            ],
            options={
                'db_table': 'monthinfo',
            },
        ),
        migrations.CreateModel(
            name='MonthCategoryInfo',
            fields=[
                ('id', models.BigAutoField(db_column='monthinfo_id', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=70)),
                ('time_spent', models.DurationField(default=datetime.timedelta(seconds=1200))),
                ('percent', models.FloatField(default=0.0)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('month_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='monthcategoryinfos', to='statisticapp.MonthInfo')),
            ],
            options={
                'db_table': 'monthcategoryinfo',
            },
        ),
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.BigAutoField(db_column='badge_id', primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
                ('sector', models.CharField(max_length=100)),
                ('lower_bound', models.FloatField(default=0.0)),
                ('upper_bound', models.FloatField(default=0.0)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('week_info', models.ManyToManyField(related_name='badges', to='statisticapp.WeekInfo')),
            ],
            options={
                'db_table': 'badge',
            },
        ),
    ]

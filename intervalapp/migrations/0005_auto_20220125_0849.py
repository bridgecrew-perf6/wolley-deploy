# Generated by Django 3.0.14 on 2022-01-25 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dailypathapp', '0004_auto_20220118_1513'),
        ('intervalapp', '0004_auto_20220124_1714'),
    ]

    operations = [
        migrations.CreateModel(
            name='IntervalMove',
            fields=[
                ('id', models.BigAutoField(db_column='intervalmove_id', primary_key=True, serialize=False)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('transport', models.CharField(max_length=70)),
                ('percent', models.FloatField(default=0.0)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('daily_path', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='intervalmoves', to='dailypathapp.DailyPath')),
            ],
            options={
                'db_table': 'intervalmove',
            },
        ),
        migrations.CreateModel(
            name='IntervalStay',
            fields=[
                ('id', models.BigAutoField(db_column='intervalstay_id', primary_key=True, serialize=False)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('address', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=70)),
                ('location', models.CharField(max_length=70)),
                ('homelike_latitude', models.FloatField()),
                ('homelike_longitude', models.FloatField()),
                ('workingplacelike_latitude', models.FloatField()),
                ('workingplacelike_longitude', models.FloatField()),
                ('percent', models.FloatField(default=0.0)),
                ('emotion', models.CharField(choices=[('positive', 'Positive'), ('normal', 'Normal'), ('negative', 'Negative')], default='normal', max_length=20, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('daily_path', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='intervalstays', to='dailypathapp.DailyPath')),
            ],
            options={
                'db_table': 'intervalstay',
            },
        ),
        migrations.DeleteModel(
            name='Interval',
        ),
    ]

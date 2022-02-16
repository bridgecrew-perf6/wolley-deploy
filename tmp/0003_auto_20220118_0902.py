# Generated by Django 3.0.14 on 2022-01-18 09:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dailypathapp', '0002_dailypath_date'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='dailypath',
            table='dailypath',
        ),
        migrations.CreateModel(
            name='GPSlog',
            fields=[
                ('id', models.BigAutoField(db_column='GPSlog_id', primary_key=True, serialize=False)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('timestamp', models.DateTimeField()),
                ('daily_path', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gps_logs.plt', to='dailypathapp.DailyPath')),
            ],
            options={
                'db_table': 'gpslog',
            },
        ),
    ]
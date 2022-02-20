# Generated by Django 3.0.14 on 2022-01-14 18:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('intervalapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.BigAutoField(db_column='label_id', primary_key=True, serialize=False)),
                ('name', models.CharField(default='?', max_length=30)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(auto_now_add=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('interval', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='intervals', to='intervalapp.Interval')),
            ],
            options={
                'db_table': 'label',
            },
        ),
    ]
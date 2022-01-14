from django.db import models

from dailypathapp.models import DailyPath


class Interval(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='interval_id')
    pie_chart = models.ForeignKey(DailyPath, on_delete=models.CASCADE, related_name='intervals')

    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now_add=True)

    # sprint#2에 추가된 속성
    latitude = models.FloatField()
    longitude = models.FloatField()

    category = models.CharField(max_length=70)
    location = models.CharField(max_length=70)
    emotion = models.TextChoices('emotion', 'positive normal negative')

    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'interval'

    def __str__(self):
        return f'{self.pie_chart} -> interval {self.id}'

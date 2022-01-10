from django.db import models

from piechartapp.models import PieChart


class Interval(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='interval_id')
    pie_chart = models.ForeignKey(PieChart, on_delete=models.CASCADE, related_name='intervals')

    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now_add=True)

    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'interval'

    def __str__(self):
        return f'{self.pie_chart} -> interval {self.id}'

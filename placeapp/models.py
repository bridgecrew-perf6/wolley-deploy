from django.db import models

from intervalapp.models import Interval


class Label(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='label_id')
    interval = models.ForeignKey(Interval, on_delete=models.CASCADE, related_name='intervals')

    name = models.CharField(max_length=30, default="?")
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now_add=True)

    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'label'

    def __str__(self):
        return f'{self.interval} -> {self.name}'

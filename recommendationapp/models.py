from django.db import models

from dailypathapp.models import DailyPath


class Recommendation(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='recommendation_id')
    pie_chart = models.ForeignKey(DailyPath, on_delete=models.CASCADE, related_name='recommendations')

    place = models.CharField(max_length=50)

    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'recommendation'

    def __str__(self):
        return f'{self.pie_chart} -> (recommendation_id: {self.id}, place: {self.place})'

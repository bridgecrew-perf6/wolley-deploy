from django.db import models

from dailypathapp.models import DailyPath


class IntervalStay(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='intervalstay_id')
    daily_path = models.ForeignKey(DailyPath, on_delete=models.CASCADE, related_name='intervalstays')

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    # sprint#2에 추가된 속성
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=100)

    category = models.CharField(max_length=70)
    location = models.CharField(max_length=70)

    homelike_latitude = models.FloatField()
    homelike_longitude = models.FloatField()
    workingplacelike_latitude = models.FloatField()
    workingplacelike_longitude = models.FloatField()

    percent = models.FloatField(default=0.0)
    EmotionType = models.TextChoices('emotion', 'positive normal negative')
    emotion = models.CharField(max_length=20, choices=EmotionType.choices, null=True, default='normal')

    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'intervalstay'

    def __str__(self):
        return f'{self.daily_path} -> (intervalstay_id: {self.id}, category: {self.category})'


class IntervalMove(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='intervalmove_id')
    daily_path = models.ForeignKey(DailyPath, on_delete=models.CASCADE, related_name='intervalmoves')

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    transport = models.CharField(max_length=70)
    percent = models.FloatField(default=0.0)

    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'intervalmove'

    def __str__(self):
        return f'{self.daily_path} -> (intervalmove_id: {self.id}, category: {self.category})'


# class TimeRange(models.Model):
#     id = models.BigAutoField(primary_key=True, db_column='timerange_id')
#     interval = models.ForeignKey(DailyPath, on_delete=models.CASCADE, related_name='timeranges')
#
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField()
#
#     date_created = models.DateTimeField(auto_now_add=True)
#     last_updated = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         db_table = 'timerange'
#
#     def __str__(self):
#         return f'{self.interval} -> (timerange_id :{self.id}, start2end : {self.start_time}-{self.end_time})'

from django.db import models

from dailypathapp.models import DailyPath
from accountapp.models import AppUser
import datetime


class Diary(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='diary_id')
    # daily_path = models.OneToOneField(
    #     DailyPath,
    #     on_delete=models.CASCADE,
    #     null=True,
    #     blank=True,
    # )
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name="diarys")  # user가 piechart를 여러 개 가질 수 있다.
    date = models.DateField(default=datetime.date.today)
    content = models.TextField()  # 속성명 변경 text -> content(내용물)

    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'diary'

    def __str__(self):
        return f'{self.daily_path} -> (diary_id: {self.id}, content : {self.content[:10]}...)'

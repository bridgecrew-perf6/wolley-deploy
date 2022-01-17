from django.db import models
from accountapp.models import AppUser
import datetime


class DailyPath(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="dailypath_id")
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name="dailypaths")  # user가 piechart를 여러 개 가질 수 있다.

    date = models.DateField(default=datetime.date.today)

    date_created = models.DateTimeField(auto_now_add=True)  # auto_now_add는 최초 저장(insert) 시에만 현재 날짜(date.today()) 를 적용
    last_updated = models.DateTimeField(auto_now=True)  # auto_now는 django model이 save 될 때마다 현재날짜(date.today()) 로 갱신

    class Meta:
        db_table = 'dailypathapp'

    def __str__(self):
        return f'({self.date}) {self.user} -> piechart {self.id}'

from django.db import models
from accountapp.models import AppUser
import datetime


class MonthInfo(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="monthinfo_id")
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name="monthinfos")

    year = models.IntegerField(default=1900)
    month_order = models.IntegerField(default=0)

    date_created = models.DateTimeField(auto_now_add=True)  # auto_now_add는 최초 저장(insert) 시에만 현재 날짜(date.today()) 를 적용
    last_updated = models.DateTimeField(auto_now=True)  # auto_now는 django model이 save 될 때마다 현재날짜(date.today()) 로 갱신

    class Meta:
        db_table = 'monthinfo'

    def __str__(self):
        return f'{self.user} -> (monthinfo_id : {self.id}, date: {self.year}-{self.month_order})'


class MonthCategoryInfo(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="monthinfo_id")
    month_info = models.ForeignKey(MonthInfo, on_delete=models.CASCADE, related_name="monthcategoryinfos")

    name = models.CharField(max_length=70)
    time_spent = models.DurationField(default=datetime.timedelta(minutes=20))
    percent = models.FloatField(default=0.0)

    date_created = models.DateTimeField(auto_now_add=True)  # auto_now_add는 최초 저장(insert) 시에만 현재 날짜(date.today()) 를 적용
    last_updated = models.DateTimeField(auto_now=True)  # auto_now는 django model이 save 될 때마다 현재날짜(date.today()) 로 갱신

    class Meta:
        db_table = 'monthcategoryinfo'

    def __str__(self):
        return f'{self.month_info} -> (monthcategoryinfo_id : {self.id}, name: {self.name})'


class WeekInfo(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="weekinfo_id")
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name="weekinfos")

    year = models.IntegerField(default=1900)
    month_order = models.IntegerField(default=0)
    week_order = models.IntegerField(default=0)

    date_created = models.DateTimeField(auto_now_add=True)  # auto_now_add는 최초 저장(insert) 시에만 현재 날짜(date.today()) 를 적용
    last_updated = models.DateTimeField(auto_now=True)  # auto_now는 django model이 save 될 때마다 현재날짜(date.today()) 로 갱신

    class Meta:
        db_table = 'weekinfo'

    def __str__(self):
        return f'{self.user} -> (weekinfo_id : {self.id}, date: {self.year}-{self.month_order}-{self.week_order})'


class WeekCategoryInfo(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="weekcategoryinfo_id")
    week_info = models.ForeignKey(WeekInfo, on_delete=models.CASCADE, related_name="weekcategoryinfos")

    name = models.CharField(max_length=70)
    date = models.DateTimeField(default=datetime.datetime.today)
    time_spent = models.DurationField(default=datetime.timedelta(minutes=20))
    percent = models.FloatField(default=0.0)
    rank = models.FloatField(default=0.0)

    date_created = models.DateTimeField(auto_now_add=True)  # auto_now_add는 최초 저장(insert) 시에만 현재 날짜(date.today()) 를 적용
    last_updated = models.DateTimeField(auto_now=True)  # auto_now는 django model이 save 될 때마다 현재날짜(date.today()) 로 갱신

    class Meta:
        db_table = 'weekcategoryinfo'

    def __str__(self):
        return f'{self.week_info} -> (weekcategoryinfo_id : {self.id}, name: {self.name})'


class Badge(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="badge_id")
    week_info = models.ManyToManyField(WeekInfo, related_name="badges")

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    sector = models.CharField(max_length=100)

    lower_bound = models.FloatField(default=0.0)
    upper_bound = models.FloatField(default=0.0)

    date_created = models.DateTimeField(auto_now_add=True)  # auto_now_add는 최초 저장(insert) 시에만 현재 날짜(date.today()) 를 적용
    last_updated = models.DateTimeField(auto_now=True)  # auto_now는 django model이 save 될 때마다 현재날짜(date.today()) 로 갱신

    class Meta:
        db_table = 'badge'

    def __str__(self):
        return f'(badge_id : {self.id}, name: {self.title})'

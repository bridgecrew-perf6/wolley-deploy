from django.contrib import admin
from .models import MonthInfo, MonthCategoryInfo, WeekInfo, WeekCategoryInfo, Badge


# Register your models here.
class MonthInfoAdmin(admin.ModelAdmin):
    search_fields = ['user__user__username', 'year']


class WeekInfoAdmin(admin.ModelAdmin):
    search_fields = ['user__user__username', 'month_order']


admin.site.register(MonthInfo, MonthInfoAdmin)
admin.site.register(MonthCategoryInfo)
admin.site.register(WeekInfo, WeekInfoAdmin)
admin.site.register(WeekCategoryInfo)
admin.site.register(Badge)
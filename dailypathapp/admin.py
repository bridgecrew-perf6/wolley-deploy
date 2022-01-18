from django.contrib import admin

from .models import DailyPath
from .models import GPSLog


# class PieChartAdmin(admin.ModelAdmin):
#     list_display = ('date_created', 'last_updated', )
#
#
# admin.site.register(PieChart, PieChartAdmin)

admin.site.register(DailyPath)
admin.site.register(GPSLog)

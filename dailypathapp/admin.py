from django.contrib import admin

from .models import DailyPath
from .models import GPSLog


class GPSLogsAdmin(admin.ModelAdmin):
    search_fields = ['daily_path__user__user__username', 'daily_path__date']


admin.site.register(DailyPath)
admin.site.register(GPSLog, GPSLogsAdmin)

from django.contrib import admin

from .models import Interval

# from .models import TimeRange


# class IntervalAdmin(admin.ModelAdmin):
#     list_display = ('date_created', 'last_updated', )
#
#
# admin.site.register(Interval, IntervalAdmin)

admin.site.register(Interval)
# admin.site.register(TimeRange)

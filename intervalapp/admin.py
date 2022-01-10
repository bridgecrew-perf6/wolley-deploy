from django.contrib import admin

from .models import Interval


# class IntervalAdmin(admin.ModelAdmin):
#     list_display = ('date_created', 'last_updated', )
#
#
# admin.site.register(Interval, IntervalAdmin)

admin.site.register(Interval)

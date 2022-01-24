from django.contrib import admin

from .models import IntervalStay
from .models import IntervalMove

# from .models import TimeRange


# class IntervalAdmin(admin.ModelAdmin):
#     list_display = ('date_created', 'last_updated', )
#
#
# admin.site.register(Interval, IntervalAdmin)

admin.site.register(IntervalStay)
admin.site.register(IntervalMove)
# admin.site.register(TimeRange)

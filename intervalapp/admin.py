from django.contrib import admin

from .models import IntervalMove
from .models import IntervalStay


class IntervalMoveAdmin(admin.ModelAdmin):
    search_fields = ['daily_path__user__user__username', 'daily_path__date']


class IntervalStayAdmin(admin.ModelAdmin):
    search_fields = ['daily_path__user__user__username', 'daily_path__date']


admin.site.register(IntervalMove, IntervalMoveAdmin)
admin.site.register(IntervalStay, IntervalStayAdmin)

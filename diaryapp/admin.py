from django.contrib import admin

from .models import Diary


# class DiaryAdmin(admin.ModelAdmin):
#     list_display = ('date_created', 'last_updated', )
#
#
# admin.site.register(Diary, DiaryAdmin)

admin.site.register(Diary)

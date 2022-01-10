from django.contrib import admin

from .models import Label


# class LabelAdmin(admin.ModelAdmin):
#     list_display = ('date_created', 'last_updated', )
#
#
# admin.site.register(Label, LabelAdmin)

admin.site.register(Label)

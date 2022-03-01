from django.contrib import admin

from .models import AppUser, Estimate

admin.site.register(AppUser)
admin.site.register(Estimate)
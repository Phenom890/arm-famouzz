from django.contrib import admin

from .models import Profile


class ProfileAdminPanel(admin.ModelAdmin):
    list_display = ['user', 'gender']


admin.site.register(Profile, ProfileAdminPanel)

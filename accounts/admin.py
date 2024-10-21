from django.contrib import admin

from .models import Profile, AdminReply


class ProfileAdminPanel(admin.ModelAdmin):
    list_display = ['user', 'gender']


class AdminReplyAdminPanel(admin.ModelAdmin):
    list_display = ['receiver', 'reply_to', 'seen', 'date_created']


admin.site.register(Profile, ProfileAdminPanel)
admin.site.register(AdminReply, AdminReplyAdminPanel)

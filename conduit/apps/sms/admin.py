from django.contrib import admin
from conduit.apps.sms.models import (Sms, Command)


class SmsAdmin(admin.ModelAdmin):
    list_display = ('id', 'time','content','sender', 'receiver', 'device',  'updatedAt')


class CommandAdmin(admin.ModelAdmin):
    list_display = ('id', 'time', 'unit', 'type', 'parameter')

admin.site.register(Sms, SmsAdmin)
admin.site.register(Command, CommandAdmin)


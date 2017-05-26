from django.contrib import admin
from conduit.apps.sms.models import Sms


class SmsAdmin(admin.ModelAdmin):
    list_display = ('id', 'time','content','sender', 'receiver', 'device',  'updated_at')


admin.site.register(Sms, SmsAdmin)


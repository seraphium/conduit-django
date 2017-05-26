from django.contrib import admin
from conduit.apps.reports.models import Report
from conduit.apps.reports.models import DeviceReport


class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'time','unit','distance1current','distance2current','distance3current', 'message', 'isalert',
                    'updated_at')

class DeviceReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'time','unit','csq','mode','protocolversion', 'hardwareversion', 'softwareversion',
                    'updated_at')


admin.site.register(Report, ReportAdmin)
admin.site.register(DeviceReport, DeviceReportAdmin)


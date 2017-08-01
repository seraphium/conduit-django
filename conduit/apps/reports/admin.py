from django.contrib import admin
from conduit.apps.reports.models import Report


class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'time','unit','usDistMsr1','usDistMsr2','usDistMsr3', 'message', 'isAlert',
                    'updated_at')


admin.site.register(Report, ReportAdmin)


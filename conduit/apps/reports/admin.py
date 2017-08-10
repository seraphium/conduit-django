from django.contrib import admin
from conduit.apps.reports.models import Report


class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'time','unit','usDistMsr1','usDistMsr2','usDistMsr3', 'message', 'isAlert',
                    'updatedAt', 'createdAt')


admin.site.register(Report, ReportAdmin)


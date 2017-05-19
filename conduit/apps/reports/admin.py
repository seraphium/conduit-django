from django.contrib import admin
from conduit.apps.reports.models import Report


class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'time','unit','distance1current','distance2current','distance3current', 'message', 'isalert')


admin.site.register(Report, ReportAdmin)


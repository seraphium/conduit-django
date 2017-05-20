from django.contrib import admin
from conduit.apps.units.models import Unit


class UnitAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phonenum','identity','towerfrom', 'towerto', 'idintower', 'parent')


admin.site.register(Unit, UnitAdmin)


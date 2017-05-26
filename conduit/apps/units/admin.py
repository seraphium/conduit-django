from django.contrib import admin
from conduit.apps.units.models import Unit
from conduit.apps.units.models import UnitNetworkSettings
from conduit.apps.units.models import UnitAlertSettings


class UnitAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phonenum','identity','towerfrom', 'towerto', 'idintower',
                    'parent', 'get_alertsettings_distance1', 'get_alertsettings_distance2',
                    'get_alertsettings_distance3', 'status', 'updated_at')

    def get_alertsettings_distance1(self, obj):
        return obj.alertsettings.alertdistance1

    get_alertsettings_distance1.short_description = 'Distance1'
    get_alertsettings_distance1.admin_order_field = 'alertsettings__distance1'

    def get_alertsettings_distance2(self, obj):
        return obj.alertsettings.alertdistance2

    get_alertsettings_distance2.short_description = 'Distance2'
    get_alertsettings_distance2.admin_order_field = 'alertsettings__distance2'

    def get_alertsettings_distance3(self, obj):
        return obj.alertsettings.alertdistance3

    get_alertsettings_distance3.short_description = 'Distance3'
    get_alertsettings_distance3.admin_order_field = 'alertsettings__distance3'

class UnitAlertSettingsAdmin(admin.ModelAdmin):
    list_display = ('unit', 'alertdistance1', 'alertdistance2', 'alertdistance3', 'picresolution', 'picenable',
                    'piclightenhance', 'highsensitivity','beep', 'weather', 'mode',
                    'camera1mode','camera1videoduration', 'camera1videoframerate', 'camera1mediainterval',
                    'camera2mode','camera2videoduration','camera2videoframerate','camera2mediainterval',
                    'camera3mode','camera3videoduration', 'camera3videoframerate','camera3mediainterval',)

class UnitNetworkSettingsAdmin(admin.ModelAdmin):
    list_display = ('unit', 'serverip', 'serverport', 'transfertype', 'networktype', 'apn',
                    'apnusername', 'apnpassword','timeout', 'retrycount', 'resetcount',
                    'csq','networkstatus')


admin.site.register(Unit, UnitAdmin)
admin.site.register(UnitAlertSettings, UnitAlertSettingsAdmin)
admin.site.register(UnitNetworkSettings, UnitNetworkSettingsAdmin)


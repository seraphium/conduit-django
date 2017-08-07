from django.contrib import admin
from conduit.apps.units.models import Unit
from conduit.apps.units.models import UnitNetworkSettings
from conduit.apps.units.models import UnitAlarmSettings
from conduit.apps.units.models import UnitCameraSettings


class UnitAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phoneNum','identity','towerFrom', 'towerTo', 'idInTower',
                    'parent', 'owner', 'get_alarmsettings_distance1', 'get_alarmsettings_distance2',
                    'get_alarmsettings_distance3', 'status', 'updatedAt')

    def get_alarmsettings_distance1(self, obj):
        return obj.alarmSettings.almDistSet1

    get_alarmsettings_distance1.short_description = 'Distance1'
    get_alarmsettings_distance1.admin_order_field = 'alarmsettings__almDistSet1'

    def get_alarmsettings_distance2(self, obj):
        return obj.alarmSettings.almDistSet2

    get_alarmsettings_distance2.short_description = 'Distance2'
    get_alarmsettings_distance2.admin_order_field = 'alarmsettings__almDistSet2'

    def get_alarmsettings_distance3(self, obj):
        return obj.alarmSettings.almDistSet3

    get_alarmsettings_distance3.short_description = 'Distance3'
    get_alarmsettings_distance3.admin_order_field = 'alarmsettings__almDistSet3'

class UnitAlarmSettingsAdmin(admin.ModelAdmin):
    list_display = ('unit', 'almDistSet1', 'almDistSet2', 'almDistSet3', 'beepEnable', 'weatherMask', 'sensMode')

class UnitNetworkSettingsAdmin(admin.ModelAdmin):
    list_display = ('unit', 'serverIp', 'serverPort')

class UnitCameraSettingsAdmin(admin.ModelAdmin):
    list_display = ('unit', 'camEnable1', 'camMode1', 'camEnable2', 'camMode2', 'camEnable3', 'camMode3')

admin.site.register(Unit, UnitAdmin)
admin.site.register(UnitAlarmSettings, UnitAlarmSettingsAdmin)
admin.site.register(UnitNetworkSettings, UnitNetworkSettingsAdmin)
admin.site.register(UnitCameraSettings, UnitCameraSettingsAdmin)


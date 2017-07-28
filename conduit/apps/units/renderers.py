from conduit.apps.core.renderers import ConduitJSONRenderer


class UnitJSONRenderer(ConduitJSONRenderer):
    object_label = 'unit'
    pagination_object_label = 'units'
    pagination_count_label = 'unitsCount'


class UnitAlarmSettingsJSONRenderer(ConduitJSONRenderer):
    object_label = 'alarmSettings'
    pagination_object_label = 'alarmSettings'
    pagination_count_label = 'alarmSettingsCount'

class UnitNetworkSettingsJSONRenderer(ConduitJSONRenderer):
    object_label = 'networkSettings'
    pagination_object_label = 'networkSettings'
    pagination_count_label = 'networkSettingsCount'

class UnitCameraSettingsJSONRenderer(ConduitJSONRenderer):
    object_label = 'cameraSettings'
    pagination_object_label = 'cameraSettings'
    pagination_count_label = 'cameraSettingsCount'

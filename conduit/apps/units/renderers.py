from conduit.apps.core.renderers import ConduitJSONRenderer


class UnitJSONRenderer(ConduitJSONRenderer):
    object_label = 'unit'
    pagination_object_label = 'units'
    pagination_count_label = 'unitsCount'


class UnitAlertSettingsJSONRenderer(ConduitJSONRenderer):
    object_label = 'alertsetting'
    pagination_object_label = 'alertsettings'
    pagination_count_label = 'alertsettingsCount'

class UnitNetworkSettingsJSONRenderer(ConduitJSONRenderer):
    object_label = 'networksetting'
    pagination_object_label = 'networksettings'
    pagination_count_label = 'networksettingsCount'

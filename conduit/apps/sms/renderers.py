from conduit.apps.core.renderers import ConduitJSONRenderer


class SmsJSONRenderer(ConduitJSONRenderer):
    object_label = 'sms'
    pagination_object_label = 'smss'
    pagination_count_label = 'smsCount'


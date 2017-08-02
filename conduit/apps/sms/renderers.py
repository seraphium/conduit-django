from conduit.apps.core.renderers import ConduitJSONRenderer


class SmsJSONRenderer(ConduitJSONRenderer):
    object_label = 'sms'
    pagination_object_label = 'smss'
    pagination_count_label = 'smsCount'

class CommandJSONRenderer(ConduitJSONRenderer):
    object_label = 'command'
    pagination_object_label = 'commands'
    pagination_count_label = 'commandCount'

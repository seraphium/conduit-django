from conduit.apps.core.renderers import ConduitJSONRenderer


class ReportJSONRenderer(ConduitJSONRenderer):
    object_label = 'reports'
    pagination_object_label = 'report'
    pagination_count_label = 'reportCount'

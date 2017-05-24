from conduit.apps.core.renderers import ConduitJSONRenderer


class ReportJSONRenderer(ConduitJSONRenderer):
    object_label = 'reports'
    pagination_object_label = 'report'
    pagination_count_label = 'reportCount'

class DeviceReportJSONRenderer(ConduitJSONRenderer):
    object_label = 'devicereports'
    pagination_object_label = 'devicereport'
    pagination_count_label = 'deviceReportsCount'
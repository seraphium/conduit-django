from conduit.apps.core.renderers import ConduitJSONRenderer
import json


class ReportJSONRenderer(ConduitJSONRenderer):
    object_label = 'reports'
    pagination_object_label = 'report'
    pagination_count_label = 'reportCount'

    def render(self, data, media_type=None,  renderer_context=None):
        if data.get('reports', None) is not None:
            return json.dumps({
                "success": True
            })
        else:
            return super(ReportJSONRenderer, self).render(data)
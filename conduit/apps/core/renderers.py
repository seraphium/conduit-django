import json
from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnList

class ConduitJSONRenderer(JSONRenderer):
    charset = 'utf-8'
    object_label = 'object'
    object_label_plural = 'objects'

    def render(self, data, media_type=None, renderer_context=None):
        if isinstance(data, ReturnList):
            listdata = super(ConduitJSONRenderer, self).render(data).decode('utf-8')
            _data = json.loads(listdata)
            return json.dumps({
                self.object_label_plural: _data
            })
        else:
            errors = data.get('error', None)
            if errors is not None:
                return super(ConduitJSONRenderer, self).render(data)

            return json.dumps({
                self.object_label: data
            })




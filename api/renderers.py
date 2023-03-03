from rest_framework import renderers
import json


class UserRender(renderers.JSONRenderer):
    charset='utf-8'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        responce=''
        if 'ErrorDetail' in str(data):
            responce=json.dumps({'errors':data})
        else:
            responce=json.dumps(data)
        return super().render(data, accepted_media_type, renderer_context)
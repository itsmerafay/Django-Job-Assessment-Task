from rest_framework import renderers
import json 

# Doing our own custom becuase we want easy/similar response format
class UserRenderer(renderers.JSONRenderer):
    charset = 'utf-8'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        
        response = ''
        # This errordetail str gets everytime there occurs error
        # When from serializer we call print(serializers.errors)
        if 'ErrorDetail' in str(data):
            response = json.dumps({
                'errors': data
            })
        else:
            response = json.dumps(data)

        return response
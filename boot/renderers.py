from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


class CustomRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        # return super().render(data, accepted_media_type, renderer_context)
        response: Response = renderer_context['response']

        """
        response, data 의 정보를 활용하여 커스텀한 응답 형태를 만들 수 있습니다.  
        """
        result_payload = {
            'result': False,
            'data': {},
            'error': {}
        }

        if (response.exception):
            result_payload['error'] = data
        else:
            result_payload['result'] = True
            result_payload['data'] = data

        renderer_context['response'].data = result_payload
        return super().render(result_payload, accepted_media_type=accepted_media_type,
                              renderer_context=renderer_context)

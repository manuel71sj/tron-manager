from http import HTTPStatus
from typing import Any, Dict, Union

from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import exception_handler


def api_exception_handler(exec, context: Dict[str, Any]) -> Union[JsonResponse, Response]:
    response = exception_handler(exec, context)

    http_code_to_message = {v.value: v.description for v in HTTPStatus}

    if response is not None:
        error_payload = {
            'status_code': 0,
            'message': '',
            'details': [],
        }

        status_code = response.status_code

        error_payload['status_code'] = status_code
        if exec is None:
            error_payload['message'] = http_code_to_message[status_code]
            error_payload['details'] = response.data
        else:
            error_payload['message'] = exec.default_code
            error_payload['details'] = exec.detail

        response.data = error_payload

    return response

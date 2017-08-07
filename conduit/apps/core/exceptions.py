from rest_framework.views import exception_handler
from rest_framework import status


def core_exception_handler(exc, context):
    response = exception_handler(exc, context)
    handlers = {
        'NotFound': _handle_not_found_error,
        'ValidationError': _handle_generic_error,
    }

    exception_class = exc.__class__.__name__
    if exception_class in handlers:
        return handlers[exception_class](exec, context, response)

    return response


def _handle_generic_error(exc, context, response):
    error = response.data.get('error', None) if isinstance(response.data, dict) else response.data
    if error is None:
        error = response.data

    response.data = {
        "success": False,
        "errors":  error
    }
    response.status_code = status.HTTP_200_OK
    return response


def _handle_not_found_error(exc, context, response):
    view = context.get('view', None)
    if view and hasattr(view,  'queryset') and view.queryset is not None:
        error_key = view.queryset.model._meta.verbose_name

        response.data = {
            'success' : False,
             error_key: response.data['detail']
        }
        response.status_code = status.HTTP_200_OK

    else:
        response = _handle_generic_error(exc, context, response)

    return response
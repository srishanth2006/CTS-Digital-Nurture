"""
Utility helpers for the Course Management API.
"""

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom DRF exception handler that ensures a consistent, informative
    error payload for every handled exception (400, 404, etc.).
    """
    response = exception_handler(exc, context)

    if response is not None:
        error_payload = {
            "error": True,
            "status_code": response.status_code,
            "details": response.data,
        }
        response.data = error_payload

    return response


def get_object_or_error_response(model_class, pk):
    """
    Helper for function-based views: fetch an object by primary key,
    returning (object, None) on success or (None, Response) on failure.
    """
    try:
        obj = model_class.objects.get(pk=pk)
        return obj, None
    except model_class.DoesNotExist:
        error_response = Response(
            {
                "error": True,
                "status_code": status.HTTP_404_NOT_FOUND,
                "details": f"{model_class.__name__} with id {pk} not found.",
            },
            status=status.HTTP_404_NOT_FOUND,
        )
        return None, error_response

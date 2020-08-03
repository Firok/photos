from rest_framework.exceptions import APIException
from rest_framework import status


class RequestError(APIException):
    """
    Raised when the key information is not included in the request.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'request_error'

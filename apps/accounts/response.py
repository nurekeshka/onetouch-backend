from rest_framework.serializers import Serializer
from rest_framework.response import Response
from rest_framework import status


class BadRequestException(Response):
    def __init__(self, message: str, data: dict or None=None):
        super().__init__(None, status=status.HTTP_400_BAD_REQUEST)

        if isinstance(data, Serializer):
            msg = (
                'You passed a Serializer instance as data, but '
                'probably meant to pass serialized `.data` or '
                '`.error`. representation.'
            )
            raise AssertionError(msg)

        self.data = _error_data(message, data) if data else _error(message)


class NotFoundException(Response):
    def __init__(self, message: str):
        super().__init__(None, status=status.HTTP_404_NOT_FOUND)
        self.data = _error(message)


class SuccessAcceptedResponse(Response):
    def __init__(self, message: str, data: dict or None=None):
        super().__init__(None, status=status.HTTP_202_ACCEPTED)

        if isinstance(data, Serializer):
            msg = (
                'You passed a Serializer instance as data, but '
                'probably meant to pass serialized `.data` or '
                '`.error`. representation.'
            )
            raise AssertionError(msg)
        
        self.data = _success_data(message, data) if data else _success(message)


class SuccessCreatedResponse(Response):
    def __init__(self, message: str, data: dict):
        super().__init__(None, status=status.HTTP_201_CREATED)

        if isinstance(data, Serializer):
            msg = (
                'You passed a Serializer instance as data, but '
                'probably meant to pass serialized `.data` or '
                '`.error`. representation.'
            )
            raise AssertionError(msg)
        
        self.data = _success_data(message, data)


def _success(message: str) -> dict:
    return {
        'success': message
    }


def _success_data(message: str, data: dict) -> dict:
    return {
        'success': message,
        'data': data
    }


def _error(message: str) -> dict:
    return {
        'error': message
    }


def _error_data(message: str, data: dict) -> dict:
    return {
        'error': message,
        'data': data
    }

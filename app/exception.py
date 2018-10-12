# coding=utf-8


class APIException(Exception):
    """Base Exception for APIs.
    """

    ERROR_CODE = None
    STATUS_CODE = 200

    def __init__(self, message, data=None, debug_message=None):
        if self.ERROR_CODE is None:
            raise NotImplementedError()
        self._message = message
        self._data = dict(data) if data else None
        self._debug_message = debug_message

    @property
    def code(self):
        return self.ERROR_CODE

    @property
    def message(self):
        return self._message

    @property
    def data(self):
        return self._data

    @property
    def debug_message(self):
        return self._debug_message


class BadRequestException(APIException):
    """
    Corresponding to HTTP code 400
    """
    ERROR_CODE = 400
    STATUS_CODE = 400

    def __init__(self, message=u'请求错误', data=None, debug_message=None):
        super(BadRequestException, self).__init__(message, data, debug_message)


class ResourceNotFoundException(APIException):
    """
    Corresponding to HTTP code 404
    """
    ERROR_CODE = 4041
    STATUS_CODE = 404

    def __init__(self, message=u'资源不存在', data=None, debug_message=None):
        super(ResourceNotFoundException, self).__init__(message, data, debug_message)


class ResourceNotAvailableException(APIException):
    """
    Corresponding to HTTP code 410
    """
    ERROR_CODE = 107
    STATUS_CODE = 410

    def __init__(self, message=u'资源不可用', data=None, debug_message=None):
        super(ResourceNotAvailableException, self).__init__(message, data, debug_message)

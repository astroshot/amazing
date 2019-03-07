# coding=utf-8
from tornado.web import HTTPError


class APIException(HTTPError):
    """Base Exception for APIs.
    """

    ERROR_CODE = None
    STATUS_CODE = 200

    def __init__(self, info, status_code, log_message=None, **kwargs):
        self._info = info
        self.reason = info
        self.status_code = status_code
        self.log_message = log_message
        self._data = dict(kwargs)

    @property
    def info(self):
        return self._info

    @property
    def data(self):
        return self._data


class BadRequestException(APIException):
    """
    Corresponding to HTTP code 400
    """
    ERROR_CODE = 400
    STATUS_CODE = 400

    def __init__(self, info=u'请求错误', status_code=STATUS_CODE, log_message=None):
        super(BadRequestException, self).__init__(info, status_code, log_message)


class ResourceNotFoundException(APIException):
    """
    Corresponding to HTTP code 404
    """
    ERROR_CODE = 4041
    STATUS_CODE = 404

    def __init__(self, info=u'请求错误', status_code=STATUS_CODE, log_message=None):
        super(ResourceNotFoundException, self).__init__(info, status_code, log_message)


class ResourceNotAvailableException(APIException):
    """
    Corresponding to HTTP code 410
    """
    ERROR_CODE = 107
    STATUS_CODE = 410

    def __init__(self, info=u'请求错误', status_code=STATUS_CODE, log_message=None):
        super(ResourceNotAvailableException, self).__init__(info, status_code, log_message)

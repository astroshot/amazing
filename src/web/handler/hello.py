# coding=utf-8
from src.web.handler import check_api_version
from src.web.handler.version import VersionHandler
from src.exception import BadRequestException


class HelloHandler(VersionHandler):
    _versions = ('1.0', '1.1')

    def __init__(self, application, request, **kwargs):
        super(HelloHandler, self).__init__(application, request, **kwargs)
        self.dispatch = {
            self._versions[0]: self.get_v1,
            self._versions[1]: self.get_v2,
        }

    @check_api_version
    def get(self, *args, **kwargs):
        current_version = self.version  # may be None
        if not current_version:
            return self.get_v1(*args, **kwargs)

        func = self.dispatch.get(current_version, None)
        if not func:
            raise BadRequestException(u'错误的 API 版本号: {} 或者映射错误'.format(current_version))

        return func(*args, **kwargs)

    def get_v1(self, *args, **kwargs):
        self.render_json({
            'msg': 'calling get_v1',
            'version': self.version,
        })

    def get_v2(self, *args, **kwargs):
        self.render_json({
            'msg': 'calling get_v2',
            'version': self.version,
        })


class HelloV2Handler(VersionHandler):
    _versions = ('1.0', '1.1', '1.3')

    @check_api_version
    def get(self, *args, **kwargs):
        self.render_json({
            'msg': 'hello'
        })

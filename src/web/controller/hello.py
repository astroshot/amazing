# coding=utf-8

from src.web.controller.version import VersionHandler


class HelloHandler(VersionHandler):

    __versions = ('1.0', '1.1')

    def get(self, *args, **kwargs):
        self.check_version(self.__versions, *args, **kwargs)
        self.render_json({
            'msg': 'hello'
        })

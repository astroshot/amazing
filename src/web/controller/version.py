# coding=utf-8
"""
"""
from src.exception import BadRequestException
from six import string_types
from tornado.web import HTTPError
from . import APIBaseHandler


class VersionHandler(APIBaseHandler):
    """VersionHandler has a tuple class attribute `__versions` which describes all versions of this handler.
    All its subclass can generate url path with each version within url path.
    Version info could be loaded from each HTTP method `*args`.

    Caution: URI path is designed with the form `/fz-py/{version}/custom/path`, So `version` is passed to HTTP method
    as args[0]
    """

    __versions = ('1.0',)

    @property
    def version(self):
        """

        :return: if not overwritten, return default version of this Handler
        """
        version = self.get_query_argument('v')
        if isinstance(version, string_types):
            return version
        else:
            return self.__versions[0]

    def get_versions(self):
        """

        :return: return supported versions of this Handler
        """
        return self.__versions

    def check_version(self, legal_versions, *args, **kwargs):
        """Check API version, make sure version in path should be legal in tuple `__versions`

        :param legal_versions:
        :param args: args passed to subclass handler from uri path
        :param kwargs:
        :return:
        """

        if len(args) < 1:
            return
        version = args[0]  # if your path is different, implements your own version check method
        if version not in legal_versions:
            raise BadRequestException(info=u'API 版本号错误: {}'.format(version))

    def get(self, *args, **kwargs):
        self.check_version(*args)

# coding=utf-8
"""
"""
from cached_property import cached_property
from src.exception import BadRequestException
from six import string_types
from . import APIBaseHandler


class VersionHandler(APIBaseHandler):
    """VersionHandler has a tuple class attribute `__versions` which describes all versions of this handler.
    All its subclass can generate url path with each version within url path.
    Version info could be loaded from each HTTP method `*args`.

    Caution: URI path is designed with the form `/fz-py/{version}/custom/path`, So `version` is passed to HTTP method
    as args[0]
    """

    _versions = ('1.0',)

    @property
    def version(self):
        """Get API version by the order of
        `uri path param` -> `query param` -> `default version`

        :return: if not overwritten, return default version of this Handler
        """
        version = getattr(self, 'current_version', None)
        if version is not None:
            return version

        version = self.get_query_argument('v', self._versions[0])
        if isinstance(version, string_types):
            return version
        return self._versions[0]

    def get_defined_versions(self):
        """

        :return: return supported versions of this Handler
        """
        return self._versions

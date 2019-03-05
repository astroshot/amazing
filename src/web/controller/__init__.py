# coding=utf-8

from cached_property import cached_property
from tornado.escape import json_decode, json_encode
from tornado.netutil import is_valid_ip
from tornado.web import RequestHandler

from src.exception import BadRequestException


class APIBaseHandler(RequestHandler):
    _MAX_CACHE_SIZE = 10000
    _METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH']
    _STATUS_CODE_REASONS = {
        422: 'Cannot be processed Entity',
    }

    # The default max page size
    # If requested limit large than this, use this instead.
    max_page_size = 20

    # handler-level authenticator
    authenticator_cls = None

    def set_default_headers(self):
        pass

    def prepare(self):
        pass

    def on_finish(self):
        pass

    @property
    def remote_ip(self):
        """We don't use Tornado ``HTTPServerRequest.remote_ip`` directly, cause
        this value depend on ``HTTPServer.xheaders`` setting. Gunicorn recent
        change (http://docs.gunicorn.org/en/latest/news.html#tornado-worker)
        make us cannot set this setting. So we first get remote IP from header.
        """
        # get remote IP from XFF hdr, fallback to request.remote_ip
        remote_ip = self.request.headers.get("X-Forwarded-For", self.request.remote_ip)
        remote_ip = remote_ip.split(',')[0].strip()

        # prefer to get remote IP from X-Real-IP hdr, fallback to XFF IP
        remote_ip = self.request.headers.get("X-Real-Ip", remote_ip)
        remote_ip = remote_ip.split(',')[0].strip()

        if is_valid_ip(remote_ip):
            return remote_ip
        return self.request.remote_ip

    _JSON_ARG_DEFAULT = object()

    def get_json_argument(self, name, default=_JSON_ARG_DEFAULT):
        """A convenient method to get json arguments. If default is not provided,
        throw a BadRequestException exception on args not found.

        :param name:
        :param default:
        :return:
        """
        try:
            return self.request_json_body[name]
        except KeyError:
            if default is self._JSON_ARG_DEFAULT:
                raise BadRequestException()

            return default
        except ValueError:
            raise BadRequestException()

    @cached_property
    def request_json_body(self):
        return json_decode(self.request.body)

    @property
    def cookies(self):
        """An alias for
        `self.request.cookies <http.util.HTTPServerRequest.cookies>`."""
        return self.request.cookies

    @property
    def user_agent(self):
        return self.request.headers.get('User-Agent', '')

    @property
    def referer(self):
        return self.request.headers.get('Referer', '')

    @property
    def x_origin_uri(self):
        return self.request.headers.get('X-Origin-RequestURI', '')

    def get_int_argument(self, name, default=None):
        arg = self.get_argument(name, '')
        if arg.isdigit():
            return int(arg)
        else:
            return default

    def options(self, *args, **kwargs):
        allow_headers = self.request.headers.get('Access-Control-Request-Headers', 'Authorization').split(',')
        allow_headers = [header.strip() for header in allow_headers]

        if self.settings['enable_cors']:
            self.write_cors_headers(self.settings['allow_origins'], self._METHODS,
                                    allow_headers, cache_max_age=60 * 60)

    def write_cors_headers(self, allow_origins=None, allow_methods=None, allow_headers=None,
                           cache_max_age=None, allow_credentials=True):
        # write CORS headers
        # see: https://developer.mozilla.org/en-US/docs/Web/HTTP/Access_control_CORS
        allow_origins = allow_origins or []
        allow_methods = allow_methods or []
        allow_headers = allow_headers or []
        origin = self.request.headers.get('Origin', None)
        if not origin:
            return
        if origin in allow_origins or '*' in allow_origins:
            self.set_header('Access-Control-Allow-Origin', origin)

            if allow_methods:
                self.set_header('Access-Control-Allow-Methods', ', '.join(allow_methods))
            if allow_headers:
                self.set_header('Access-Control-Allow-Headers', ', '.join(allow_headers))
            if cache_max_age:
                self.set_header('Access-Control-Max-Age', cache_max_age)
            if allow_credentials:
                self.set_header('Access-Control-Allow-Credentials', 'true')

    def render_json(self, data):
        self.set_header('Content-Type', 'application/json')
        self.finish(json_encode(data))

    @property
    def protocol(self):
        protocol = self.request.headers.get('X-Forwarded-Proto', '')
        protocol = protocol.lower()
        return protocol if protocol == 'https' else 'http'


class AllowCrossDomainHandler(APIBaseHandler):

    def set_default_headers(self):
        super(AllowCrossDomainHandler, self).set_default_headers()
        self.set_header('Access-Control-Allow-Origin', self.request.headers.get('Origin', ''))
        self.set_header('Access-Control-Allow-Methods',
                        ', '.join(['GET', 'PATCH', 'PUT', 'POST', 'DELETE', 'OPTIONS']))
        self.set_header("Access-Control-Allow-Headers", self.request.headers.get("access-control-request-headers", ""))
        self.set_header("Access-Control-Allow-Credentials", "true")

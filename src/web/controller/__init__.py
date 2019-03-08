# coding=utf-8

from cached_property import cached_property
from functools import wraps
from tornado.escape import json_decode, json_encode
from tornado.netutil import is_valid_ip
from tornado.web import RequestHandler

from src.exception import APIException, BadRequestException


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
        self.finish(json_encode(data).encode('utf-8'))

    @property
    def protocol(self):
        protocol = self.request.headers.get('X-Forwarded-Proto', '')
        protocol = protocol.lower()
        return protocol if protocol == 'https' else 'http'

    def send_error(self, status_code=500, **kwargs):
        """Sends the given HTTP error code to the browser.

        If `flush()` has already been called, it is not possible to send
        an error, so this method will simply terminate the response.
        If output has been written but not yet flushed, it will be discarded
        and replaced with the error page.

        Override `write_error()` to customize the error page that is returned.
        Additional keyword arguments are passed through to `write_error`.
        """
        if self._headers_written:
            gen_log.error("Cannot send error response after headers written")
            if not self._finished:
                # If we get an error between writing headers and finishing,
                # we are unlikely to be able to finish due to a
                # Content-Length mismatch. Try anyway to release the
                # socket.
                try:
                    self.finish()
                except Exception:
                    print("Failed to flush partial response",
                          exc_info=True)
            return
        self.clear()

        reason = kwargs.get('reason')
        if 'exc_info' in kwargs:
            exception = kwargs['exc_info'][1]
            if isinstance(exception, APIException) and exception.reason:
                reason = exception.reason
        self.set_status(status_code)
        try:
            self.render_json({
                'code': exception.ERROR_CODE if isinstance(exception, APIException) else -1,
                'info': reason,
                'data': exception.data if isinstance(exception, APIException) else None,
            })
        except Exception:
            print("Uncaught exception in write_error", exc_info=True)
        if not self._finished:
            self.finish()


class AllowCrossDomainHandler(APIBaseHandler):

    def set_default_headers(self):
        super(AllowCrossDomainHandler, self).set_default_headers()
        self.set_header('Access-Control-Allow-Origin', self.request.headers.get('Origin', ''))
        self.set_header('Access-Control-Allow-Methods',
                        ', '.join(['GET', 'PATCH', 'PUT', 'POST', 'DELETE', 'OPTIONS']))
        self.set_header("Access-Control-Allow-Headers", self.request.headers.get("access-control-request-headers", ""))
        self.set_header("Access-Control-Allow-Credentials", "true")


def check_api_version(func):
    """Check API Version of Handler Instance
    usage: Just decorate it to the method you required. After check, an attribute named as `current_version` is bound
    to handler with selected version in path.

    :param func: HTTP method implemented by `RequestHandler`
    :return: func(*args, **kwargs)
    """
    _inject_name = 'current_version'

    def decorator(func):
        @wraps(func)
        def http_method(*args, **kwargs):
            argc = len(args)
            if argc < 1:
                return func(*args, **kwargs)

            instance = args[0]  # handler instance
            setattr(instance, _inject_name, None)
            if argc == 1:  # No uri path arguments
                return func(*args, **kwargs)

            # if your path is different, get your version in your own way
            version = args[1]
            if version not in instance.get_defined_versions():
                raise BadRequestException(u'错误的 API 版本号: {}'.format(version))
            setattr(instance, _inject_name, version)
            return func(*args, **kwargs)

        return http_method

    return decorator(func)

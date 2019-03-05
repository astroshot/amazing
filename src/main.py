# coding=utf-8
import tornado
import tornado.httpserver
from tornado.options import options, define
from tornado.web import Application

from src.web.urls import handlers

define('port', default=8000, help='listening port', type=int)


def parse_cmd_params():
    try:
        tornado.options.parse_command_line()
    except Exception as e:
        print(e)


def get_application():
    settings = {
        'gzip': True,
        'debug': True,
        'enable_cors': True,
        'allow_origins': [],
    }

    _app = Application(handlers, **settings)
    return _app


def main():
    parse_cmd_params()
    app = get_application()
    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    http_server.bind(options.port)
    http_server.start()
    print('server started listening: {}'.format(options.port))
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()

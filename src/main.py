# coding=utf-8
import os

import tornado
import tornado.httpserver
from tornado.options import options, define
from tornado.web import Application

from src.const import CONF_PATH
from src.util.singleton import Config

define('port', default=8000, help='listening port', type=int)
define('env', default='dev', help='server env', type=str)


def parse_cmd_params():
    try:
        tornado.options.parse_command_line()
    except Exception as e:
        print(e)


def get_application():
    from src.web.urls import handlers
    settings = {
        'gzip': True,
        'debug': True,
        'enable_cors': True,
        'allow_origins': [],
    }

    app = Application(handlers, **settings)
    return app


def main():
    parse_cmd_params()
    env = options.env
    config_file = '{path}/{env}.toml'.format(path=CONF_PATH, env=env)
    if not os.path.exists(config_file):
        raise RuntimeError('Config file not found: {}', config_file)
    conf = Config()
    conf.put('env', env)
    conf.put('config_file', config_file)

    # handlers must bu imported after config
    app = get_application()
    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    http_server.bind(options.port)
    http_server.start()
    print('server started listening: {}'.format(options.port))
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()

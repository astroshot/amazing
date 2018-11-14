# coding=utf-8
from app.web.view.echo import EchoHandler
from app.web.view.hello import HelloHandler

handlers = [
    (r'/', HelloHandler),
    (r'/hello', HelloHandler),
    (r'/echo', EchoHandler),
]

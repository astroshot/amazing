# coding=utf-8
from app.web.view.hello import HelloHandler

handlers = [
    (r'/', HelloHandler),
    (r'/hello', HelloHandler),
]

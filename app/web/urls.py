# coding=utf-8
from app.web.controller.echo import EchoHandler
from app.web.controller.hello import HelloHandler
from app.web.controller.upload_images import UploadImagesHandler

handlers = [
    (r'/', HelloHandler),
    (r'/hello', HelloHandler),
    (r'/echo', EchoHandler),
    (r'/images/actions/upload', UploadImagesHandler),
]

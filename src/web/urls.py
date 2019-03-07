# coding=utf-8
from src.web.controller.echo import EchoHandler
from src.web.controller.hello import HelloHandler
from src.web.controller.upload_images import UploadImagesHandler

handlers = [
    (r'/', HelloHandler),
    (r'/hello', HelloHandler),
    (r'/hello/(\d+\.\d+)', HelloHandler),
    (r'/echo', EchoHandler),
    (r'/images/actions/upload', UploadImagesHandler),
]

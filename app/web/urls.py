# coding=utf-8
from app.web.view.echo import EchoHandler
from app.web.view.hello import HelloHandler
from app.web.view.upload_images import UploadImagesHandler

handlers = [
    (r'/', HelloHandler),
    (r'/hello', HelloHandler),
    (r'/echo', EchoHandler),
    (r'/images/actions/upload', UploadImagesHandler),
]

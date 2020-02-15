# coding=utf-8
from src.web.handler.echo import EchoHandler
from src.web.handler.hello import HelloHandler, HelloV2Handler
from src.web.handler.upload_images import UploadImagesHandler
from src.web.handler.user import UserHandler

handlers = [
    (r'/', HelloHandler),
    (r'/hello', HelloHandler),
    (r'/hello/(\d+\.\d+)', HelloHandler),
    (r'/hello2/(\d+\.\d+)', HelloV2Handler),
    (r'/echo', EchoHandler),
    (r'/images/actions/upload', UploadImagesHandler),
    (r'/users', UserHandler),

]

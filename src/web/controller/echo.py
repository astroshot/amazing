# coding=utf-8
from src.web.controller import APIBaseHandler


class EchoHandler(APIBaseHandler):

    def post(self):
        name = self.get_body_argument('name', 'default name')
        msg = 'Hello {}!'.format(name)
        self.render_json({
            'msg': msg,
        })

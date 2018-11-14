# coding=utf-8
from app.web.view import APIBaseHandler


class EchoHandler(APIBaseHandler):

    def post(self):
        name = self.get_body_argument('name', 'default name')
        msg = 'Hello {}!'.format(name)
        self.render_json({
            'msg': msg,
        })

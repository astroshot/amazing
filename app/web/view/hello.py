# coding=utf-8

from app.web.view import APIBaseHandler


class HelloHandler(APIBaseHandler):

    def get(self):
        self.render_json({
            'msg': 'hello'
        })

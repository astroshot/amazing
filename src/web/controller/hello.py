# coding=utf-8

from src.web.controller import APIBaseHandler


class HelloHandler(APIBaseHandler):

    def get(self):
        self.render_json({
            'msg': 'hello'
        })

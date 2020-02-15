# coding=utf-8
"""
"""
from src.dao.user.user import UserDAO
from src.web.handler import APIBaseHandler


class UserHandler(APIBaseHandler):

    def post(self):
        name = self.get_json_argument('name')
        phone_no = self.get_json_argument('phone_no')
        email = self.get_json_argument('email')
        user_type = self.get_json_argument('type')

        user = UserDAO.add(name, phone_no, email, user_type)
        self.render_json({'info': True})

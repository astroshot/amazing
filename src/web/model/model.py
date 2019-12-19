# coding=utf-8
"""
"""
import json


class BaseVO(json.JSONEncoder):

    def default(self, o):
        d = {'__class__': o.__class__.__name__, '__module__': o.__module__}
        d.update(o.__dict__)
        return d


class User(BaseVO):

    def __init__(self, name, age):
        self.name = name
        self.age = age


if __name__ == '__main__':
    u = User("Kevin", 20)
    us = json.dumps(u, cls=BaseVO)
    print(us)

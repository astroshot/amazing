# coding=utf-8
"""
"""


class JSONObject(dict):
    """JSONObject allows you to get key using `obj.key`

    """
    __slots__ = ()

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as e:
            raise AttributeError(e)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError as e:
            raise AttributeError(e)

    def __repr__(self):
        return '<JSONObject ' + dict.__repr__(self) + '>'

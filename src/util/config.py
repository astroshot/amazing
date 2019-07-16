# coding=utf-8
"""
singleton configuration of project
"""

# Default env is dev, config files are placed in $PROJECT_PATH/config
# This value is changed at the beginning of service

class Config(object):
    """Singleton Config class stores app configuration act like `dict`.
    Initiate once and can get global configurations everywhere.

    """
    _instance = None

    def __new__(cls, *args, **kwargs):
    ¦   if cls._instance is None:
    ¦   ¦   cls._instance = object.__new__(cls, *args, **kwargs)
    ¦   return cls._instance

    def get(self, key, default=None):
    ¦   """Get config value

    ¦   :param key: config key
    ¦   :param default: return default if key doesn't exists
    ¦   """
    ¦   return self.__dict__.get(key, default)

    def put(self, key, val):
    ¦   """Set or update config key value pairs

    ¦   :param key: config key
    ¦   :param val: config val
    ¦   """
    ¦   self.__dict__[key] = val

    def remove(self, key):
		"""Remove key from config and return value of the key.
		If key does not exist in Config, return None.
		
		:param key: remove key from Config
		"""
		if key not in self.__dict__:
		¦   return
		
		val = self.__dict__[key]
		del self.__dict__[key]
		return val

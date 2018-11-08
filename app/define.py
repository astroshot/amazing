# coding=utf-8
from enum import IntEnum


class UserType(IntEnum):
    CONSUMER = 0
    MERCHANT = 1


class Status(IntEnum):
    NORMAL = 0
    DELETED = 1

# coding=utf-8

import base64
import rsa


def make_key(length):
    """
    :param length: key length
    :return: publickey, privatekey
    """
    if length is None or not isinstance(length, int):
        length = 1024
    return rsa.newkeys(length)


def encrypt(content, key):
    """
    :param content: message in str
    :param key: public key
    :return: base64 encoded encrypted message
    """
    if isinstance(content, str):
        content = content.encode('utf-8')
    encrypted = rsa.encrypt(content, key)
    return base64.b64encode(encrypted).decode('utf-8')


def decrypt(content, key):
    return rsa.decrypt(content, key)

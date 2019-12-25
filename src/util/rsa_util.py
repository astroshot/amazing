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
    content = base64.b64decode(content.encode('utf-8'))
    decrypted_content = rsa.decrypt(content, key)
    return decrypted_content.decode('utf-8')


def __example():
    pub_key, private_key = make_key(1024)
    content = u'人生如逆旅，我亦是行人'
    encrypted_str = encrypt(content, pub_key)
    decrypted_str = decrypt(encrypted_str, private_key)
    info = 'public key: {}, private_key: {}, encrypted text: {}, decrypted text: {}'.format(
        pub_key.save_pkcs1(), private_key.save_pkcs1(), encrypted_str, decrypted_str
    )
    print(info)


if __name__ == '__main__':
    __example()


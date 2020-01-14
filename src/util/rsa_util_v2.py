# coding=utf-8


import hashlib
import base64
import time
import json

import requests
from Crypto import Random
from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.PublicKey import RSA


def generate_key_pair(key_len=1024):
    """Generate RSA key pair
    :param key_len: length of key, generaly 1024, 2048
    """
    random_generator = Random.new().read
    rsa = RSA.generate(key_len, random_generator)
    private_pem = rsa.exportKey()
    public_pem = rsa.publickey().exportKey()
    return private_pem, public_pem


def encrypt(content, key):
    rsakey = RSA.importKey(key)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    cipher_text = cipher.encrypt(content.encode())
    return base64.b64encode(cipher_text)


def decrypt(cipher_text, key):
    random_generator = Random.new().read
    rsakey = RSA.importKey(key)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    cipher_text = base64.b64decode(cipher_text)
    return cipher.decrypt(cipher_text, random_generator)


def sign(content, key):
    rsakey = RSA.importKey(key)
    signer = Signature_pkcs1_v1_5.new(rsakey)
    digest = SHA.new()
    digest.update(content.encode())
    sign = signer.sign(digest)
    signature = base64.b64encode(sign)
    return signature


def verify(content, signature, key):
    rsakey = RSA.importKey(key)
    verifier = Signature_pkcs1_v1_5.new(rsakey)
    digest = SHA.new()
    # Assumes the data is base64 encoded to begin with
    digest.update(content.encode())
    return verifier.verify(digest, base64.b64decode(signature))


def main():
    private_key_str = """-----BEGIN RSA PRIVATE KEY-----\nMIICdQIBADANBgkqhkiG9w0BAQEFAASCAl8wggJbAgEAAoGBAL6aVlkAKPjzMdQpJKoG/TayQYR/en/6lmlY0wi44KA/KDlWn+iZJKwGZQEU/TGwOSJz5QQwQkGqS2BwTZo/IhmXzgONajflcO2llPXCTjpdkPuuNvOUPgNzPeV9bYXwQlR9Ta1VFK4sgGtotvQ8bIJQ96bzf7zcJDOva8R9JaZtAgMBAAECgYA34ukOj41z8Vra6nVlpUb5kqrDPt2cSM1xdinqlMrIMbyJk2yvtreZ+QYEmzLiLtmR0ImGAOBsgJI5ZLRcVcaZWOywSQjmex3zYbey7nplIZBtDLC7wtI3SuP/ZS49O896ozux7RPA57ekQXufuD0kQf4OxB4VblOa4zYHLWw7wQJBAN/nQLX+9Q91pQBjWUe7Zr5Fx1iYz+BJGcnkiUddEX8NvC9+Li+pGGd+7ILgCEWPhcJC9/ZdpuBCPY/ZxqKhfisCQQDZ7Qh3lvbmH1O72pTvobMQMTfIicbu0Iqh84xDGSl9nL3/Elvbzk2R8qDhk/mOCE3IA4qCnE9e4TL+u2soDznHAkAyobS8cx8vk8bwQ4cY9YPSWy0tF8FKUr2GLivs+1rNhGmdw8bl+DMQlF8faVH1iPMSbtpr19m4tMH/GZwVgrdpAkA1DQDsq/F639Fwf6uWElUW8gRUa0XkSRwWhMV2aB+zln6iI4P9JGG5z8jeYTl1HAxjTolfdlHUFRpm7JUPcXVtAkBv3izp87NqkeFIc7vs+vDmVRKSS0j4O7R0VipUZNux/QDJ/RnriV2SuPzRoKng32nCZ8xM5G72FUxghaTrn8+2\n-----END RSA PRIVATE KEY-----"""
    pub_key_str = """MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC+mlZZACj48zHUKSSqBv02skGEf3p/+pZpWNMIuOCgPyg5Vp/omSSsBmUBFP0xsDkic+UEMEJBqktgcE2aPyIZl84DjWo35XDtpZT1wk46XZD7rjbzlD4Dcz3lfW2F8EJUfU2tVRSuLIBraLb0PGyCUPem83+83CQzr2vEfSWmbQIDAQAB"""

    sign_body = 'message'
    privkey = RSA.importKey(private_key_str)
    signer = Signature_pkcs1_v1_5.new(privkey)
    digest = SHA.new()
    digest.update(sign_body.encode())
    sign = signer.sign(digest)
    sign = base64.b64encode(sign)
    print(sign)

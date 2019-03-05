# coding=utf-8
from os.path import splitext


def get_file_extension(file_path):
    extension = ''
    if file_path:
        extension = splitext(file_path)[1]
    return extension

# coding=utf-8
import unittest

from app.util.file_util import get_file_extension


class TestFileUtil(unittest.TestCase):

    def test_file_extension(self):
        filename = '/path/readme.txt'
        ext = get_file_extension(filename)
        self.assertEqual('.txt', ext)

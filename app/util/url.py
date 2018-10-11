#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import string
import urllib


def make_url(domain, uri, uri_prefix='', protocol='http'):
    """

    :param domain: port should be inside if port provided.
    :param uri:
    :param uri_prefix:
    :param protocol:
    :return:
    """
    domain = string.rstrip(domain, '/')
    uri = '/' + string.lstrip(uri, '/')
    if uri_prefix:
        uri_prefix = '/' + string.strip(uri_prefix, '/')

    return '{protocol}://{domain}{uri_prefix}{uri}'.format(
        protocol=protocol, domain=domain, uri_prefix=uri_prefix, uri=uri
    )


def gen_uri(path, query_arguments=None):
    """

    :param path:
    :param query_arguments:
    :return:
    """
    if not query_arguments:
        return path

    return '{path}?{query}'.format(path=path, query=urllib.urlencode(query_arguments, doseq=True))

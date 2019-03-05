#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from urllib import parse


def make_url(domain, uri, uri_prefix='', protocol='http'):
    """

    :param domain: port should be inside if port provided.
    :param uri:
    :param uri_prefix:
    :param protocol:
    :return:
    """
    domain = domain.rstrip('/')
    uri = '/' + uri.lstrip('/')
    if uri_prefix:
        uri_prefix = '/' + uri_prefix.strip('/')

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

    return '{path}?{query}'.format(path=path, query=parse.urlencode(query_arguments, doseq=True))

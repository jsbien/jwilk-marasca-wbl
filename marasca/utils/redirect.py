# encoding=UTF-8

# Copyright © 2009, 2010 Jakub Wilk <jwilk@jwilk.net>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 dated June, 1991.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.

import base64
import hashlib
import urllib

import django.http
from django.conf import settings

def protect_url(url):
    key = hash_url(url)
    if django.VERSION < (1, 6):
        # https://docs.djangoproject.com/en/1.6/releases/1.6/#quoting-in-reverse
        quoted_url = urllib.quote(url, safe='/:')
    else:
        quoted_url = url
    if quoted_url.startswith('http://'):
        tail = quoted_url[7:]
    else:
        raise ValueError(quoted_url)
    return django.core.urlresolvers.reverse(safe_redirect, kwargs=dict(key=key, scheme='http', tail=tail))

def hash_url(url):
    digest = hashlib.md5(settings.SECRET_KEY + url).digest()
    return base64.urlsafe_b64encode(digest)[:5]

def safe_redirect(request, key, scheme, tail):
    url = '%s://%s' % (scheme, tail)
    if key != hash_url(url):
        raise django.http.Http404
    return django.http.HttpResponseRedirect(url)

# vim:ts=4 sw=4 et

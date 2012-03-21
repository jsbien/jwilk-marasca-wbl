# encoding=UTF-8

# Copyright © 2009, 2010, 2011 Jakub Wilk <jwilk@jwilk.net>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 dated June, 1991.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.

from django.conf.urls.defaults import *
import django.views.generic.simple

from app import views, snippets, coordinates
from utils import redirect

urlpatterns = patterns('',
    # technical stuff
    url(r'^ping/', views.process_ping),
    url(r'^redirect/(?P<key>[A-Za-z0-9_-]+)/(?P<scheme>http)/(?P<tail>.*)$', redirect.safe_redirect),
    url(r'^i18n/set-language/', views.set_language),
    url(r'^google([0-9a-f]+[.]html)', 'django.views.static.serve', dict(document_root='media/google/'), name='css'),
    # media
    url(r'^css/(?P<path>.*)$', 'django.views.static.serve', dict(document_root='media/css/'), name='css'),
    url(r'^js/(?P<path>.*)$', 'django.views.static.serve', dict(document_root='media/js/'), name='js'),
    url(r'^extra/(?P<path>.*)$', 'django.views.static.serve', dict(document_root='media/extra/'), name='extra'),
    # translatable content
    url(r'^$', views.process_index, name='index'),
    url(r'^help/$', views.process_help, name='help'),
    url(r'^(?P<corpus_id>[\w-]+)/$', views.corpus_info, name='corpus'),
    url(r'^(?P<corpus_id>[\w-]+)/query/(?P<page_start>[0-9]+)[+]/$', views.process_query, dict(query=True), name='query'),
    url(r'^(?P<corpus_id>[\w-]+)/query/(?P<nth>[0-9]+)/$', views.process_query, dict(query=True), name='query'),
    url(r'^(?P<corpus_id>[\w-]+)/query/$', views.process_query, dict(query=True), name='query'),
    url(r'^(?P<corpus_id>[\w-]+)/query/(?:[0-9]+[+]?/)?m(?P<nth>[0-9]+)/$', views.process_metadata_snippet),
    url(r'^(?P<corpus_id>[\w-]+)/snippet/(?P<volume>[1-9][0-9]*)/(?P<page>[1-9][0-9]*)/(?P<x>[0-9]+),(?P<y>[0-9]+),(?P<w>[1-9][0-9]*),(?P<h>[1-9][0-9]*)/$', snippets.view, name='snippet'),
    url(r'^(?P<corpus_id>[\w-]+)/coordinates/(?P<n_from>(?:0|[1-9][0-9]*))-(?P<n_to>(?:0|[1-9][0-9]*))', coordinates.view),
    url(r'^error/404/', django.views.generic.simple.direct_to_template, dict(template='404.html')),
    url(r'^error/500/', django.views.generic.simple.direct_to_template, dict(template='500.html')),
)

# vim:ts=4 sw=4 et

#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Tommy.Yu'
SITENAME = u"Tommy's Notes"
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = u'zh'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = ()

# Social widget
SOCIAL = ()

DEFAULT_PAGINATION = 20

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

PLUGIN_PATHS=['/Users/h/pelican-plugins']
THEME='pelican-bootstrap3'
PLUGINS = ['i18n_subsites', 'tipue_search' ]
JINJA_ENVIRONMENT = {
    'extensions': ['jinja2.ext.i18n'],
}

USE_FOLDER_AS_CATEGORY = True

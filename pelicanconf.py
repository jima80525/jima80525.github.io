#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = 'Jim Anderson'
SITENAME = 'Snowboarding Coder'
SITESUBTITLE = 'Musing on writing code'
SITEURL = ''
PATH = 'content'
TIMEZONE = 'America/Denver'
DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DEFAULT_PAGINATION = 10

MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
    },
    'output_format': 'html5',
}


PLUGINS = [
            'minchin.pelican.plugins.nojekyll',
          ]

USE_FOLDER_AS_CATEGORY = False
DEFAULT_CATEGORY = 'Posts'

YEAR_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/{date:%b}/index.html'

# JHA TODO REmove this flag for Dev only
# LOAD_CONTENT_CACHE = False

RELATIVE_URLS = True

THEME = 'pelican-twitchy'
PYGMENTS_STYLE = "monokai"
BOOTSTRAP_THEME = 'darkly'
EXPAND_LATEST_ON_INDEX = True
SHARE = True
SOCIAL = (('Twitter', 'https://twitter.com/jimande75053775'), ('GitHub', 'https://github.com/jima80525'))
DISPLAY_CATEGORIES_ON_MENU = False
CC_LICENSE = 'CC-BY-SA'

# these were 2nd place themse for twitchy
# BOOTSTRAP_THEME = 'cyborg'
# BOOTSTRAP_THEME = 'litera'
# BOOTSTRAP_THEME = 'slate'
# need to change pygments style to match bootstrap style
# PYGMENTS_STYLE = "xcode"  # doesn't work with darkly

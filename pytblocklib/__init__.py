"""
a python library for youtube blocking functions without using yt api, Selenium, or BeautifulSoup.

This program uses a customized `browser_cookie3` library.
The original copyright of `browser_cookie 3` belongs to borisbabic : 
https://github.com/borisbabic/browser_cookie3
"""
__copyright__    = 'Copyright (C) 2020 taizan-hokuto'
__version__      = '0.1.1'
__license__      = 'GNU Lesser General Public License v3 (LGPLv3)'
__author__       = 'taizan-hokuto'
__author_email__ = '55448286+taizan-hokuto@users.noreply.github.com'
__url__          = 'https://github.com/taizan-hokuto/pytblocklib'


RELEASE = True

from .watcher import Watcher
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- python -*-
from __future__ import print_function

__license__ = """

The MIT License (MIT)
Copyright (c) 2013 Jacob Smith <kloptops@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

from bs4 import BeautifulSoup

from lockfile import LockFile
import plex
from plex import LockFile, PlexServerConnection



def main():
    import json

    conn = PlexServerConnection('norti-pc.local', 32400)


    sections_page = conn.fetch('library/sections')
    sections_soup = BeautifulSoup(sections_page)

    for section_tag in sections_soup.find_all('directory'):
        key = section_tag['key']

        print('{0:#^40}'.format("[ " + section_tag['title'] + " ]"))
        items_page = conn.fetch('library/sections/{0}/all'.format(key))
        items_soup = BeautifulSoup(items_page)
        
        ratings = [[] for i in range(plex.RATING_UNKNOWN+1)]        

        for item in items_soup.find_all('directory'):
            string_rating = item.get('contentrating', '')
            if string_rating not in plex.content_ratings:
                print(u"Unknown content rating {0!r} for {1}".format(
                    string_rating, item.get('title')))
                return
            
            content_rating = plex.content_ratings[string_rating]
            ratings[content_rating].append(item.get('title'))
        for item in items_soup.find_all('video'):
            string_rating = item.get('contentrating', '')
            if string_rating not in plex.content_ratings:
                print(u"Unknown content rating {0!r} for {1}".format(
                    string_rating, item.get('title')))
                return
            
            content_rating = plex.content_ratings[string_rating]
            ratings[content_rating].append(item.get('title'))

        for rating, shows in enumerate(ratings):
            if len(shows) == 0:
                continue
            print(u"  {0}".format(plex.RATING_NAMES[rating]))
            for show in shows:
                print(u"    {0}".format(show))
            print('')

if __name__ == '__main__':
    # Probably doesn't need this...
    with LockFile() as lf:
	   main()

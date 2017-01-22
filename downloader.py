# -*- coding: utf8 -*-

# Author: Birger Schulze

import urllib2
import os


def download(url):
    return urllib2.urlopen(url)


def downloadCurl(url, filename):
    os.system('curl -s -A {} -o {} {}'.format("Mozilla/5.0", filename, url))


def showWebsite(url):
    for line in url:
        print(line)

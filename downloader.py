 # -*- coding: utf8 -*-

import urllib2
import os

def download(url):
    return urllib2.urlopen(url)

def downloadCurl(url, filename):
    r = os.system('curl -A {} -o {} {} -s'.format("Mozilla/5.0", filename, url))

def showWebsite(url):
    for line in url:
        print(line)


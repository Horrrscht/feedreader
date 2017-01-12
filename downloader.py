 # -*- coding: utf8 -*-

import urllib2

def download(url):
    return urllib2.urlopen(url)

def showWebsite(url):
    for line in url:
        print line


# -*- coding: utf8 -*-

import json
from downloader import *
from rss2json import *

def getFeedList():
    return json.load(open("feedlist.json"))["feeds"] #TODO: Error-Check

def reloadFeed(name, url):
    pass

def getFeed(name):
    feedlist = open("feedlist.json", "r")
    source = json.load(feedlist)
    feedlist.close()
    for feed in source["feeds"]:
        if feed["name"] == name:
            if feed["file"] == None:
                filename = "{}.json".format(name)
                xmlFile = "{}.xml".format(name)
                downloadCurl(feed["url"], xmlFile)
                file = open(filename, "w")
                file.write(dict2json(rss2dict(xmlFile)))
                file.close()
                feed["file"] = filename
                feedlist = open("feedlist.json", "w")
                feedlist.write(dict2json(source))
                feedlist.close()
                return getFeed(name)
            return json.load(open(feed["file"]))
    return None #TODO: Error if feed not in feedlist

#print(getFeedList())

print(getFeed("XKCD"))
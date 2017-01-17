# -*- coding: utf8 -*-

import json
from downloader import *
from rss2json import *


def getFeedList():
    return json.load(open("feedlist.json"))["feeds"]  # TODO: Error-Check


def reloadFeed(name, url, feedDict, sourceDict):
    filename = "{}.json".format(name)
    xmlFile = "{}.xml".format(name)
    downloadCurl(url, xmlFile)
    file = open(filename, "w")
    file.write(dict2json(rss2dict(xmlFile)))
    file.close()
    feedDict["file"] = filename
    feedlist = open("feedlist.json", "w")
    feedlist.write(dict2json(sourceDict))
    feedlist.close()


pass


def getFeed(name):
    feedlist = open("feedlist.json", "r")
    source = json.load(feedlist)
    feedlist.close()
    for feed in source["feeds"]:
        if feed["name"] == name:
            if feed["file"] == None:
                reloadFeed(name, feed["url"], feed, source)
                return getFeed(name)
            return json.load(open(feed["file"]))
    return None  # TODO: Error if feed not in feedlist


# print(getFeedList())

getFeed("XKCD")

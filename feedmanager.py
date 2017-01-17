# -*- coding: utf8 -*-

import json

def getFeedList():
    return json.load(open("feedlist.json"))["feeds"] #TODO: Error-Check



def getFeed(name):
    source = json.load(open("feedlist.json"))["feeds"]
    for feed in source:
        if feed["name"] == name:
            return json.load(open(feed["file"]))
    return None #TODO: Error if feed not in feedlist

#print(getFeedList())

getFeed("ARD")
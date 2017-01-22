# -*- coding: utf8 -*-

# Author: Birger Schulze

from xml.dom import minidom
import json
import sys


def xmlValue(root, tagname):
    item = root.getElementsByTagName(tagname)
    if not item:
        return None
    return item[0].firstChild.wholeText


def channelInfo(channelRoot):
    return {"title": xmlValue(channelRoot, "title"),
            "link": xmlValue(channelRoot, "link"),
            "description": xmlValue(channelRoot, "description")}


def itemInfo(itemRoot):
    return {"title": xmlValue(itemRoot, "title"),
            "link": xmlValue(itemRoot, "link"),
            "description": xmlValue(itemRoot, "description"),
            "guid": xmlValue(itemRoot, "guid")
            }


def rss2dict(rssFile):
    root = minidom.parse(rssFile)
    rssRoot = root.getElementsByTagName("rss")[0]  # TODO: Check if it's proper rss
    channelRoot = rssRoot.getElementsByTagName("channel")[0]
    info = channelInfo(channelRoot)
    items = channelRoot.getElementsByTagName("item")
    itemInfos = [itemInfo(item) for item in items]
    return {"channelInfo": info, "items": itemInfos}


def dict2json(inputDict):
    return json.dumps(inputDict, indent=4, separators=(",", ":"))

    # print(dict2json(rss2dict(sys.argv[1])))

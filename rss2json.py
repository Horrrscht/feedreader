 # -*- coding: utf8 -*-

from xml.dom import minidom
import json

def xmlValue(root, tagname):
    item = root.getElementsByTagName(tagname)
    if not item:
        return None
    if item == None:
        return None
    return item[0].firstChild.wholeText

def channelInfo(channelRoot):
    return {"title":xmlValue(channelRoot, "title"), 
            "link":xmlValue(channelRoot, "link"), 
            "description":xmlValue(channelRoot, "description")}

def itemInfo(itemRoot):
    return {"title":xmlValue(itemRoot, "title"), 
            "link":xmlValue(itemRoot, "link"), 
            "description":xmlValue(itemRoot, "description"),
            "guid":xmlValue(itemRoot, "guid")
            }

root = minidom.parse("testdata/ardtest")

rssRoot = root.getElementsByTagName("rss")[0]
channelRoot = rssRoot.getElementsByTagName("channel")[0]

info = channelInfo(channelRoot)
items = channelRoot.getElementsByTagName("item")
itemInfos = [itemInfo(item) for item in items] 
feedContent = {"channelInfo":info,"items":itemInfos}

#print(json.dumps(info, indent=4, separators=(",",":")))
#print(json.dumps(itemInfos, indent=4, separators=(",",":")))
print(json.dumps(feedContent, indent=4, separators=(",",":")))

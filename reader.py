#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author: Birger Schulze

import sys

import curses
from curses.textpad import rectangle

from feedmanager import getFeed, getFeedList
import locale

locale.setlocale(locale.LC_ALL, '')

keyBindTexts = [
    "> Switch to textfield",
    "< Switch to feedlist",
    "q Quit",
    "r Reload selected feed [WIP]"
]

def formatText(item):
    desc = item["description"] if item["description"] != None else "No description"
    title = item["title"] if item["title"] != None else "No title"
    link = item["link"] if item["link"] != None else "No link"
    return title + "\n\n" + desc + "\n\n" + link  # TODO: Scheiß encoding-fails

def inputLoop(stdscr,
              feedListWin,
              feedContentWin,
              activeWin,
              feedNames,
              feedTexts,
              feedWindowHeight,
              feedListHeight,
              selectedItem,
              selectedFeed,
              feedListDims,
              feedContentDims):
    feedOffset = 0
    textLine = 0
    ch = ""
    while (ch != "q"):
        stdscr.refresh()
        feedListWin.move(0, 0)
        for line in range(0, len(feedNames)):
            feedListWin.move(line, 0)
            if line == selectedFeed:
                feedListWin.addnstr(feedNames[line].encode('utf-8'),
                                    feedListDims[3],
                                    curses.A_STANDOUT)
            else:
                feedListWin.addnstr(feedNames[line].encode('utf-8'),
                                    feedListDims[3])
        feedContentWin.move(0, 0)
        feedContentWin.addstr(feedTexts[selectedItem].encode('utf-8'))

        feedListWin.refresh(feedOffset,
                            0,
                            feedListDims[0],
                            feedListDims[1],
                            feedListDims[0] + feedListHeight,
                            feedListDims[1] + feedListDims[3])
        feedContentWin.refresh(textLine,
                               0,
                               feedContentDims[0],
                               feedContentDims[1],
                               feedContentDims[0] + feedWindowHeight,
                               feedContentDims[1] + feedContentDims[3])
        ch = stdscr.getkey()
        if ch == "KEY_LEFT" and activeWin == feedContentWin:
            activeWin = feedListWin
        elif ch == "KEY_RIGHT" and activeWin == feedListWin:
            activeWin = feedContentWin
        elif ch == "KEY_UP" and activeWin == feedListWin and selectedFeed > 0:
            selectedItem = 0
            selectedFeed -= 1
            feedContentWin.move(0, 0)
            feedContentWin.addstr(" " * (100 * 66 - 1))
            feedTexts = [formatText(item) for item in getFeed(feedNames[selectedFeed],
                                                              forceReload=False)["items"]]
            if feedOffset > 0:
                feedOffset -= 1
        elif ch == "KEY_DOWN" and activeWin == feedListWin and selectedFeed < len(feedNames) - 1:
            selectedFeed += 1
            selectedItem = 0
            feedContentWin.move(0, 0)
            feedContentWin.addstr(" " * (100 * 66 - 1))
            feedTexts = [formatText(item) for item in getFeed(feedNames[selectedFeed],
                                                              forceReload=False)["items"]]
            if selectedFeed >= feedListHeight:
                feedOffset += 1
        elif ch == "KEY_UP" and activeWin == feedContentWin and textLine > 0:
            textLine -= 1
        elif ch == "KEY_DOWN" and activeWin == feedContentWin:  # TODO: Anzahl Zeilen zählen
            textLine += 1
        elif ch == "KEY_NPAGE" and selectedItem < len(feedTexts) - 1:
            selectedItem += 1
            feedContentWin.move(0, 0)
            feedContentWin.addstr(" " * (100 * 66 - 1))
        elif ch == "KEY_PPAGE" and selectedItem > 0:
            selectedItem -= 1
            feedContentWin.move(0, 0)
            feedContentWin.addstr(" " * (100 * 66 - 1))

def main(stdscr):
    stdscr.addstr(0, 0, "Welcome to my super-awesome feedreader")
    feedWindowHeight = 10
    feedListHeight = 5
    selectedItem = 0
    selectedFeed = 0
    feedListDims = (2, 1, 20, 25)  # y,x,height,width
    feedContentDims = (feedListDims[0] + feedListHeight + 3,
                       1,
                       100,
                       66)  # TODO: Set dimensions dynamically according to terminal size
    feedListWin = curses.newpad(feedListDims[2], feedListDims[3])
    feedContentWin = curses.newpad(feedContentDims[2], feedContentDims[3])
    activeWin = feedContentWin
    feedList = getFeedList()
    assert (feedList != None), "Error: Could not find file feedlist.json"
    feedNames = [feeds["name"] for feeds in feedList]
    feedTexts = [formatText(item) for item in getFeed(feedNames[selectedFeed],
                                                      forceReload=True)["items"]]
    rectangle(stdscr,
              feedListDims[0] - 1,
              feedListDims[1] - 1,
              feedListDims[0] + feedListHeight + 1,
              feedListDims[1] + feedListDims[3] + 1)
    rectangle(stdscr,
              feedContentDims[0] - 1,
              feedContentDims[1] - 1,
              feedContentDims[0] + feedWindowHeight + 1,
              feedContentDims[1] + feedContentDims[3] + 1)
    stdscr.move(2, feedListDims[3] + 4)
    for line in range(0, len(keyBindTexts)):
        stdscr.addstr(keyBindTexts[line])
        stdscr.move(3 + line, feedListDims[3] + 4)
    inputLoop(stdscr,
              feedListWin,
              feedContentWin,
              activeWin,
              feedNames,
              feedTexts,
              feedWindowHeight,
              feedListHeight,
              selectedItem,
              selectedFeed,
              feedListDims,
              feedContentDims
    )

if __name__ == "__main__":
    curses.wrapper(main)

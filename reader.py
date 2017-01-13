# -*- coding: utf8 -*-

import curses
from curses.textpad import rectangle

lorem = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Lorem ipsum dolor sit amet,"

feeds = ["Hello", "World", "Bla", "Blubb", "Wurst", "Kaese", "Quark"]
feedListDims = (2, 1, 6, 25)  # y,x,height,width
feedContentDims = (
feedListDims[0] + feedListDims[2] + 3, 1, 10, 66)  # TODO: Set dimensions dynamically according to terminal size


def main(stdscr):
    selectedFeed = 0
    feedOffset = 0
    textLine = 0
    stdscr.addstr(0, 0, "Welcome to my super-awesome feedreader")

    feedListWin = curses.newwin(feedListDims[2], feedListDims[3], feedListDims[0], feedListDims[1])
    feedContentWin = curses.newwin(feedContentDims[2], feedContentDims[3], feedContentDims[0], feedContentDims[1])
    activeWin = feedContentWin

    rectangle(stdscr, feedListDims[0] - 1, feedListDims[1] - 1, feedListDims[0] + feedListDims[2],
              feedListDims[1] + feedListDims[3] + 1)
    rectangle(stdscr, feedContentDims[0] - 1, feedContentDims[1] - 1, feedContentDims[0] + feedContentDims[2],
              feedContentDims[1] + feedContentDims[3] + 1)

    ch = ""
    while (ch != "q"):
        stdscr.refresh()
        feedListWin.move(0, 0)
        for line in range(0, feedListDims[2] if len(feeds) > feedListDims[2] else len(feeds)):
            feedListWin.move(line, 0)
            if line + feedOffset == selectedFeed:
                feedListWin.addnstr(feeds[feedOffset:][line], feedListDims[3], curses.A_STANDOUT)
            else:
                feedListWin.addnstr(feeds[feedOffset:][line], feedListDims[3])

        feedContentWin.move(0, 0)
        feedContentWin.addnstr(lorem[textLine * feedContentDims[3]:],
                               feedContentDims[2] * feedContentDims[3] - 1)  # TODO: Ist das so richtig?
        # Der hat anscheinend probleme mit Zeilenumbrüchen

        feedListWin.refresh()
        feedContentWin.refresh()
        ch = stdscr.getkey()

        if ch == "KEY_LEFT" and activeWin == feedContentWin:
            activeWin = feedListWin
            feedListWin.move(0, 0)
        elif ch == "KEY_RIGHT" and activeWin == feedListWin:
            activeWin = feedContentWin
            feedContentWin.move(0, 0)
        elif ch == "KEY_UP" and activeWin == feedListWin and selectedFeed > 0:
            selectedFeed -= 1
            if feedOffset > 0:
                feedOffset -= 1
        elif ch == "KEY_DOWN" and activeWin == feedListWin and selectedFeed < feedListDims[2]:
            selectedFeed += 1
            if selectedFeed >= feedListDims[2]:
                feedOffset += 1
        elif ch == "KEY_UP" and activeWin == feedContentWin and textLine > 0:
            textLine -= 1
        elif ch == "KEY_DOWN" and activeWin == feedContentWin and textLine < len(lorem) / feedContentDims[3] - \
                feedContentDims[2]:  # TODO: Anzahl Zeilen zählen
            textLine += 1


curses.wrapper(main)

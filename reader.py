 # -*- coding: utf8 -*-

import curses
from curses.textpad import rectangle

lorem = """Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.   

Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Lorem ipsum dolor sit amet,"""

texts = ["Hello", "World", "Bla", "Blubb", "Wurst", "Kaese", "Quark"]
feedListDims = (2, 1, 6, 25) #y,x,height,width
feedContentDims = (feedListDims[0]+feedListDims[2]+3, 1, 10, 66) #TODO: Set dimensions dynamically according to terminal size
selectedFeed = 0

def main(stdscr):
    stdscr.addstr(0, 0, "Welcome to my super-awesome feedreader")

    feedListWin = curses.newwin(feedListDims[2] ,feedListDims[3], feedListDims[0], feedListDims[1])
    feedContentWin = curses.newwin(feedContentDims[2] ,feedContentDims[3], feedContentDims[0], feedContentDims[1])

    rectangle(stdscr, feedListDims[0]-1, feedListDims[1]-1, feedListDims[0]+feedListDims[2], feedListDims[1]+feedListDims[3]+1)
    rectangle(stdscr, feedContentDims[0]-1, feedContentDims[1]-1, feedContentDims[0]+feedContentDims[2], feedContentDims[1]+feedContentDims[3]+1)

    ch = ""
    stdscr.refresh()
    while (ch != "q"):
        feedListWin.move(0, 0)
        for line in range(0, feedListDims[2] if len(texts) > feedListDims[2] else len(texts)):
            feedListWin.move(line, 0)
            if line == selectedFeed:          
                feedListWin.addnstr(texts[line], feedListDims[3], curses.A_STANDOUT)
            else:
                feedListWin.addnstr(texts[line], feedListDims[3])

        feedContentWin.move(0, 0)
        feedContentWin.addnstr(lorem, feedContentDims[2]*feedContentDims[3]-1)
        feedListWin.refresh()
        feedContentWin.refresh()
        ch = feedListWin.getkey()

curses.wrapper(main)

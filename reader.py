# -*- coding: utf8 -*-

import curses
from curses.textpad import rectangle

keyBindTexts = [
    "> Switch to textfield",
    "< Switch to feedlist",
    "q Quit",
    "r Reload selected feed"
]

feedText = """Spielregeln für die neue Medienwelt

Stets Zugriff auf Nachrichten aus aller Welt haben, sich mit Freunden austauschen oder nachts einkaufen gehen - das Internet bietet unzählige Möglichkeiten. Doch es drohen auch Gefahren: so können Nutzer zu viele Informationen von sich preisgeben oder sich sogar in der Virtualität verlieren. Was sie benötigen, ist Medienkompetenz - zum Beispiel im Umgang mit sozialen Netzwerken. ARD.de zeigt, welche Anforderungen die neue Medienwelt an uns stellt.

http://www.ard.de/home/ard/Medienkompetenz/76910/index.html
"""

feeds = ["Hello", "World", "Bla", "Blubb", "Wurst", "Kaese", "Quark"]
feedListDims = (2, 1, 6, 25)  # y,x,height,width
feedContentDims = (
    feedListDims[0] + feedListDims[2] + 3, 1, 50, 66)  # TODO: Set dimensions dynamically according to terminal size


def main(stdscr):
    feedWindowHeight = 15
    selectedFeed = 0
    feedOffset = 0
    textLine = 0
    stdscr.addstr(0, 0, "Welcome to my super-awesome feedreader")

    feedListWin = curses.newwin(feedListDims[2], feedListDims[3], feedListDims[0], feedListDims[1])
    #feedContentWin = curses.newwin(feedContentDims[2], feedContentDims[3], feedContentDims[0], feedContentDims[1])
    feedContentWin = curses.newpad(feedContentDims[2], feedContentDims[3])
    activeWin = feedContentWin

    rectangle(stdscr, feedListDims[0] - 1, feedListDims[1] - 1, feedListDims[0] + feedListDims[2],
              feedListDims[1] + feedListDims[3] + 1)
    rectangle(stdscr, feedContentDims[0] - 1, feedContentDims[1] - 1, feedContentDims[0] + feedWindowHeight+1,
              feedContentDims[1] + feedContentDims[3] + 1)

    stdscr.move(2, 28)
    for line in range(0, len(keyBindTexts)):
        stdscr.addstr(keyBindTexts[line])
        stdscr.move(3 + line, 28)

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
        #feedContentWin.addnstr(feedText[textLine * feedContentDims[3]:],
        #                       feedContentDims[2] * feedContentDims[3] - 1) # TODO: Ist das so richtig?
                                                                            # TODO: Der hat anscheinend probleme mit Zeilenumbrüchen
                                                                            # Das liegt daran, dass Zeilenumbrüche die Anzahl der Zeichen pro Textfeld runtersetzen
        feedContentWin.addstr(feedText)

        feedListWin.refresh()
        feedContentWin.refresh(textLine, 0, feedContentDims[0], feedContentDims[1], feedContentDims[0]+feedWindowHeight, feedContentDims[1]+feedContentDims[3])
        ch = stdscr.getkey()

        if ch == "KEY_LEFT" and activeWin == feedContentWin:
            activeWin = feedListWin
            feedListWin.move(0, 0)
            curses.curs_set(0)
        elif ch == "KEY_RIGHT" and activeWin == feedListWin:
            activeWin = feedContentWin
            feedContentWin.move(0, 0)
            curses.curs_set(2)
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
        elif ch == "KEY_DOWN" and activeWin == feedContentWin:  # TODO: Anzahl Zeilen zählen
            textLine += 1


curses.wrapper(main)

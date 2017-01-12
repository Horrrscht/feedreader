 # -*- coding: utf8 -*-

import curses
from curses.textpad import Textbox, rectangle

texts = ["Hello", "World", "Bla", "Blubb"]

def main(stdscr):
    stdscr.addstr(0, 0, "Welcome to the super-awesome feedreader")

    editwin = curses.newwin(5,30, 2,1)
    rectangle(stdscr, 0, 0, 10, 10)
    rectangle(stdscr, 20, 10, 30, 20)
    editwin.move(1, 1)
    ch = "a"
    while (ch != "q"):
        stdscr.refresh()
        editwin.refresh()
        editwin.addstr(texts[0])
        ch = editwin.getkey()
        #print(ch)

curses.wrapper(main)

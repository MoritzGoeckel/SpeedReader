import curses
import sys
import math
import time

C_RED = 1
C_YELLOW = 2

# read stdin

stdscr = curses.initscr()

height, width = stdscr.getmaxyx()
textWidth = min(57, width)
leftMargin = math.floor((width - textWidth) / 2)
topMargin = min(4, math.floor(leftMargin / 6))

def start():
    global stdscr, C_RED, C_YELLOW
    curses.start_color()
    curses.init_pair(C_RED, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(C_YELLOW, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.clear()

def shutdown():
    global stdscr
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()
    sys.exit(0)

# Get point of focus for word
def getOrp(txt):
    size = len(txt)
    if size < 2: return 0
    if size < 6: return 1
    if size < 10: return 2
    if size < 14: return 3
    return 4

def write(txt):
    global stdscr, height, width, topMargin, leftMargin
    midx = int(round(width / 2))
    midy = int(round(height / 2))

    # Clear
    stdscr.addstr(midy, midx - 5, "                    ")
    stdscr.addstr(midy + 1, midx - 5, "                    ")

    stdscr.addstr(midy, midx, "V", curses.color_pair(C_RED))

    orp = getOrp(txt)
    if len(txt) == 1:
        stdscr.addstr(midy + 1, midx, txt, curses.color_pair(C_RED))

    if len(txt) == 2:
        stdscr.addstr(midy + 1, midx, txt[0], curses.color_pair(C_RED))
        stdscr.addstr(midy + 1, midx + 1, txt[1])

    if len(txt) >= 3:
        stdscr.addstr(midy + 1, midx - orp, txt)
        stdscr.addstr(midy + 1, midx, txt[orp], curses.color_pair(C_RED))

    stdscr.move(0,0)
    stdscr.refresh()

start()
with open("sample_text.txt") as file:
    for line in file:
        for w in line.split():
            write(w)
            time.sleep(60 / 500)
            #stdscr.getch()
shutdown()

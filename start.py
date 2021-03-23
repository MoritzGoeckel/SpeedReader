import curses
import sys
import math
import time
import threading

C_RED = 1
C_YELLOW = 2

# read stdin

stdscr = curses.initscr()

height, width = stdscr.getmaxyx()
textWidth = min(57, width)
leftMargin = math.floor((width - textWidth) / 2)
topMargin = min(4, math.floor(leftMargin / 6))

wpm = 200
pause = False

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
    midy = int(round(height / 2)) - 4

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

    footer = "Running @ " + str(wpm) + " wpm"
    pos = midx - int(round(len(footer) / 2))
    stdscr.addstr(midy + 7, pos, footer)
    stdscr.addstr(midy + 8, pos, "</> to change wpm")
    stdscr.addstr(midy + 9, pos, "space to pause")
    stdscr.addstr(midy + 10, pos, "q to quit")

    stdscr.refresh()
    stdscr.move(0,0)

def iterateText():
    global stdscr, wpm, pause
    start()
    while True:
        with open("sample_text.txt") as file:
            for line in file:
                for w in line.split():
                    stdscr.clear()
                    write(w)
                    time.sleep(60 / wpm)
                    while pause: time.sleep(0.05)

reading = threading.Thread(target=iterateText)
reading.setDaemon(True)
reading.start()

while True:
    c = chr(stdscr.getch())
    if c == '>': wpm += 40
    if c == '<' and wpm > 100: wpm -= 40
    if c == ' ': pause = not pause
    if c == 'q':
        shutdown()
        exit()


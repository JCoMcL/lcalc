#!/bin/env python3

import sys
import curses
from numpy import matrix

def startcurses():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    return stdscr
def endcurses(stdscr):
    stdscr.clear()
    curses.nocbreak()
    curses.echo()
    curses.endwin()

def string2num(s):
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return 0

def read_matrix(a = None):
    stdscr = startcurses()
    if a is None:
        a = [[""]]
    else:
        a[-1][-1] = str(a[-1][-1])
        show_matrix(a, stdscr)
    while True:
        c = stdscr.getkey()
        if c == ' ' and (len(a) == 1 or len(a[-1]) < len(a[0])):
            a[-1][-1] = string2num(a[-1][-1])
            a[-1].append("")
        
        elif c == '\n' or c == ' ': #return
            #exit function by pressing return twice
            if a[-1][0] is not None:
                a.pop()
                endcurses(stdscr)
                return matrix(a)

            a[-1][-1] = string2num(a[-1][-1])
            #ensure that the column count matches
            while len(a[-1]) < len(a[0]):
                a[-1].append(0)

            a.append([""])

        elif c == '\x7f': #backspace
            pass

        else:
            a[-1][-1] += c
        show_matrix(a, stdscr)

def elems2strings(a):
    if isinstance(a, list):
        return [elems2strings(elem) for elem in a]
    else:
        return str(a)

def col_widths(mat):
    cw = [0 for i in range(len(mat[0]))]
    for row in mat:
        for i in range(len(row)):
            if len(row[i]) > cw[i]:
                cw[i] = len(row[i])
    return cw


def show_matrix(mat, stdscr):
    smat = elems2strings(mat)
    cw = col_widths(smat)
    for i in range(len(smat)):
        stdscr.addstr(i, 0, " ".join( [smat[i][j].ljust(cw[j]) for j in range(len(smat[i]))]))

if __name__ == "__main__":
    print(read_matrix())

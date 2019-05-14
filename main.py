#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wourld import Wourld
from room import Room

def main(args):
    r_list = [[4, 11, 5, 1], [7, 3, 5, 1]]
    for i in range(1):
        w = Wourld(r_list, i)
        w.combine2Rooms()
        w.draw()
        #input("Press Enter to continue...")


    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

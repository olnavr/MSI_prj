#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wourld import Wourld
from room import Room
from anime import Anime


def main(args):
    r_list = [[12, 11, 6, 4], [17, 7, 6, 3]]
    w = Wourld(r_list, 3)
    w.combine2Rooms()
    anime = Anime(w)
    input()
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

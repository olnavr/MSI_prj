#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wourld import Wourld
from room import Room
from anime import Anime


def main(args):
    r_list = [[12, 11, 5, 3], [17, 7, 5, 3]]
    w = Wourld(r_list, 3)
    w.combine2Rooms()
    w.agent.backtracking_algorithm(w)
    w.agent.backtracking_algorithm(w)
    track = w.agent.track[0] + w.agent.track[1]
    for t in track:
        print(t)
    anime = Anime(w)
    input()
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

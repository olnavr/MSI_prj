#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wourld import Wourld
from room import Room
from anime import Anime
from agent import Agent

def main(args):
    r_list = [[12, 11, 10, 8], [17, 7, 10, 8]]
    w = Wourld(r_list, 6)
    w.combine2Rooms()
    w.calcTargets()
    agent = Agent(w.agent_sp, w.targets)
    if not agent.backtracking_algorithm(w):
        print("NIE UDAŁO SIĘ ZNALEŹĆ ŚCIEŻKI")
    else:
        if not agent.backtracking_algorithm(w):
            print("NIE UDAŁO SIĘ ZNALEŹĆ ŚCIEŻKI")
        else:
            track = agent.track[0] + agent.track[1]
            for t in track:
                print(t)
    anime = Anime(w, agent)
    input()
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
